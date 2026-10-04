import 'dart:convert';
import 'package:flutter/material.dart';
import 'package:geolocator/geolocator.dart';
import 'package:http/http.dart' as http;
import 'package:shared_preferences/shared_preferences.dart';

void main() {
  runApp(const APlusGisApp());
}

class APlusGisApp extends StatelessWidget {
  const APlusGisApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'A+ Malawi GIS',
      debugShowCheckedModeBanner: false,
      theme: ThemeData(
        brightness: Brightness.dark,
        primaryColor: const Color(0xFF008751),
        scaffoldBackgroundColor: const Color(0xFF0A0F0B),
      ),
      home: const GisHomePage(),
    );
  }
}

class GisHomePage extends StatefulWidget {
  const GisHomePage({super.key});

  @override
  State<GisHomePage> createState() => _GisHomePageState();
}

class _GisHomePageState extends State<GisHomePage> with SingleTickerProviderStateMixin {
  final TextEditingController _nameController = TextEditingController();
  final TextEditingController _landmarkController = TextEditingController();

  String _latitude = "Not Captured Yet";
  String _longitude = "Not Captured Yet";
  bool _isCapturing = false;
  bool _isSending = false;
  String _statusMessage = "READY FOR FIELD CAPTURE";

  final String _tunnelUrl = "https://ab566cad61eac672-137-115-5-18.serveousercontent.com";

  late AnimationController _marqueeController;

  @override
  void initState() {
    super.initState();
    _marqueeController = AnimationController(
      duration: const Duration(seconds: 14),
      vsync: this,
    )..repeat();
    _syncOfflineQueueToServer();
  }

  @override
  void dispose() {
    _marqueeController.dispose();
    _nameController.dispose();
    _landmarkController.dispose();
    super.dispose();
  }

  Future<void> _captureCurrentLocation() async {
    setState(() {
      _isCapturing = true;
      _statusMessage = "ACQUIRING GPS SATELLITE LOCK...";
    });

    try {
      bool serviceEnabled = await Geolocator.isLocationServiceEnabled();
      if (!serviceEnabled) {
        setState(() {
          _statusMessage = "LOCATION SERVICES DISABLED";
          _isCapturing = false;
        });
        _showErrorDialog("Location services are disabled. Please turn on GPS.");
        return;
      }

      LocationPermission permission = await Geolocator.checkPermission();
      if (permission == LocationPermission.denied) {
        permission = await Geolocator.requestPermission();
        if (permission == LocationPermission.denied) {
          setState(() {
            _statusMessage = "PERMISSION DENIED";
            _isCapturing = false;
          });
          _showErrorDialog("Location permission was denied.");
          return;
        }
      }

      if (permission == LocationPermission.deniedForever) {
        setState(() {
          _statusMessage = "PERMISSION PERMANENTLY DENIED";
          _isCapturing = false;
        });
        _showErrorDialog("Location permissions are permanently denied in settings.");
        return;
      }

      Position position = await Geolocator.getCurrentPosition(
        desiredAccuracy: LocationAccuracy.high,
      );

      setState(() {
        _latitude = position.latitude.toStringAsFixed(6);
        _longitude = position.longitude.toStringAsFixed(6);
        _statusMessage = "POSITION LOCKED SUCCESSFULLY";
        _isCapturing = false;
      });

      _showSuccessSummaryDialog();
    } catch (e) {
      setState(() {
        _statusMessage = "ERROR ACQUIRING GPS";
        _isCapturing = false;
      });
      _showErrorDialog("Failed to get location: $e");
    }
  }

  Future<void> _savePinLocally(Map<String, dynamic> payload) async {
    final prefs = await SharedPreferences.getInstance();
    List<String> offlineQueue = prefs.getStringList('offline_gis_queue') ?? [];
    offlineQueue.add(jsonEncode(payload));
    await prefs.setStringList('offline_gis_queue', offlineQueue);
  }

  Future<void> _submitDataToServer() async {
    if (_latitude == "Not Captured Yet" || _longitude == "Not Captured Yet") {
      _showErrorDialog("Please capture your GPS location first before submitting.");
      return;
    }

    if (_nameController.text.trim().isEmpty) {
      _showErrorDialog("Please enter the Structure / Shop Identity Name.");
      return;
    }

    setState(() {
      _isSending = true;
      _statusMessage = "TRANSMITTING TO SERVER...";
    });

    final url = Uri.parse('$_tunnelUrl/api/save_node');

    final Map<String, dynamic> payload = {
      "name": _nameController.text.trim(),
      "landmark": _landmarkController.text.trim(),
      "latitude": _latitude,
      "longitude": _longitude,
    };

    try {
      final response = await http.post(
        url,
        headers: {"Content-Type": "application/json"},
        body: jsonEncode(payload),
      ).timeout(const Duration(seconds: 10));

      setState(() {
        _isSending = false;
        _statusMessage = "READY FOR FIELD CAPTURE";
      });

      if (response.statusCode == 200 || response.statusCode == 201) {
        _showServerResponseDialog("Success!", "Data sent directly to the central server!");
        _nameController.clear();
        _landmarkController.clear();
        _syncOfflineQueueToServer();
      } else {
        _handleOfflineFallback(payload, "Server rejected payload (Code ${response.statusCode})");
      }
    } catch (e) {
      // Shows exact exception details for troubleshooting
      _handleOfflineFallback(payload, "Exception: $e");
    }
  }

  Future<void> _handleOfflineFallback(Map<String, dynamic> payload, String reason) async {
    await _savePinLocally(payload);
    setState(() {
      _isSending = false;
      _statusMessage = "SAVED LOCALLY (OFFLINE MODE)";
    });

    _showServerResponseDialog(
        "Saved Offline Safely",
        "$reason. Your pin has been stored securely on your phone and will sync automatically when connection returns."
    );

    _nameController.clear();
    _landmarkController.clear();
  }

  Future<void> _syncOfflineQueueToServer() async {
    final prefs = await SharedPreferences.getInstance();
    List<String> offlineQueue = prefs.getStringList('offline_gis_queue') ?? [];

    if (offlineQueue.isEmpty) return;

    final url = Uri.parse('$_tunnelUrl/api/save_node');
    List<String> remainingQueue = [];

    for (String item in offlineQueue) {
      try {
        final payload = jsonDecode(item);
        final response = await http.post(
          url,
          headers: {"Content-Type": "application/json"},
          body: jsonEncode(payload),
        ).timeout(const Duration(seconds: 5));

        if (response.statusCode != 200 && response.statusCode != 201) {
          remainingQueue.add(item);
        }
      } catch (_) {
        remainingQueue.add(item);
      }
    }

    await prefs.setStringList('offline_gis_queue', remainingQueue);
  }

  void _showSuccessSummaryDialog() {
    showDialog(
      context: context,
      builder: (context) => AlertDialog(
        title: const Text("Field Data & GPS Captured"),
        content: Text(
          "Structure / Place Name:\n${_nameController.text.isEmpty ? '[Not entered yet]' : _nameController.text}\n\n"
          "Visual Landmark Clues:\n${_landmarkController.text.isEmpty ? '[Not entered yet]' : _landmarkController.text}\n\n"
          "GPS Coordinates:\nLAT: $_latitude\nLON: $_longitude"
        ),
        actions: [
          TextButton(onPressed: () => Navigator.pop(context), child: const Text("OK")),
        ],
      ),
    );
  }

  void _showServerResponseDialog(String title, String content) {
    showDialog(
      context: context,
      builder: (context) => AlertDialog(
        title: Text(title),
        content: Text(content),
        actions: [
          TextButton(onPressed: () => Navigator.pop(context), child: const Text("OK")),
        ],
      ),
    );
  }

  void _showErrorDialog(String error) {
    showDialog(
      context: context,
      builder: (context) => AlertDialog(
        title: const Text("Operation Error"),
        content: Text(error),
        actions: [
          TextButton(onPressed: () => Navigator.pop(context), child: const Text("OK")),
        ],
      ),
    );
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text("A+ MALAWI GIS COIL", style: TextStyle(fontWeight: FontWeight.bold, fontSize: 17)),
        backgroundColor: const Color(0xFF008751),
        centerTitle: true,
        toolbarHeight: 46,
      ),
      body: SafeArea(
        child: SingleChildScrollView(
          padding: const EdgeInsets.symmetric(horizontal: 14.0, vertical: 8.0),
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.stretch,
            children: [
              Container(
                height: 55,
                decoration: BoxDecoration(
                  borderRadius: BorderRadius.circular(6),
                  border: Border.all(color: Colors.greenAccent.withOpacity(0.3)),
                ),
                child: Column(
                  children: [
                    Expanded(
                      child: Container(
                        decoration: const BoxDecoration(
                          color: Colors.black,
                          borderRadius: BorderRadius.vertical(top: Radius.circular(5)),
                        ),
                        child: Center(
                          child: ClipRect(
                            child: AnimatedBuilder(
                              animation: _marqueeController,
                              builder: (context, child) {
                                return FractionalTranslation(
                                  translation: Offset(-_marqueeController.value, 0),
                                  child: const Text(
                                    "A+ MALAWI GIS • TIZIWANE KOMWE TIKUKHALA • A+ MALAWI GIS • TIZIWANE KOMWE TIKUKHALA •",
                                    style: TextStyle(color: Colors.redAccent, fontSize: 11, fontWeight: FontWeight.bold),
                                  ),
                                );
                              },
                            ),
                          ),
                        ),
                      ),
                    ),
                    Expanded(
                      child: Container(
                        color: const Color(0xFFCE1126),
                        child: const Center(
                          child: Text("REGISTER FOR EASLY SERVICE DELIVARY", style: TextStyle(color: Colors.white, fontSize: 10, fontWeight: FontWeight.bold)),
                        ),
                      ),
                    ),
                    Expanded(
                      child: Container(
                        decoration: const BoxDecoration(
                          color: Color(0xFF008751),
                          borderRadius: BorderRadius.vertical(bottom: Radius.circular(5)),
                        ),
                      ),
                    ),
                  ],
                ),
              ),
              const SizedBox(height: 8),
              Container(
                padding: const EdgeInsets.symmetric(vertical: 8, horizontal: 10),
                decoration: BoxDecoration(
                  color: const Color(0xFF111A13),
                  borderRadius: BorderRadius.circular(5),
                  border: Border.all(color: Colors.green.shade800),
                ),
                child: Text(
                  _statusMessage,
                  textAlign: TextAlign.center,
                  style: const TextStyle(fontWeight: FontWeight.bold, color: Colors.greenAccent, fontSize: 12),
                ),
              ),
              const SizedBox(height: 8),
              TextField(
                controller: _nameController,
                decoration: const InputDecoration(
                  labelText: "Structure / Population Place Name",
                  border: OutlineInputBorder(),
                  isDense: true,
                  contentPadding: EdgeInsets.all(10),
                ),
              ),
              const SizedBox(height: 8),
              TextField(
                controller: _landmarkController,
                decoration: const InputDecoration(
                  labelText: "Visual Landmark Clues / Anchors",
                  border: OutlineInputBorder(),
                  isDense: true,
                  contentPadding: EdgeInsets.all(10),
                ),
              ),
              const SizedBox(height: 8),
              Container(
                padding: const EdgeInsets.symmetric(horizontal: 6, vertical: 10),
                decoration: BoxDecoration(
                  color: Colors.grey.shade900,
                  borderRadius: BorderRadius.circular(6),
                  border: Border.all(color: Colors.amber, width: 1.2),
                ),
                child: Row(
                  mainAxisAlignment: MainAxisAlignment.spaceAround,
                  children: [
                    Expanded(
                      child: Text(
                        "LAT: $_latitude",
                        textAlign: TextAlign.center,
                        overflow: TextOverflow.ellipsis,
                        style: const TextStyle(fontFamily: 'monospace', fontSize: 11, fontWeight: FontWeight.bold, color: Colors.amber),
                      ),
                    ),
                    Expanded(
                      child: Text(
                        "LON: $_longitude",
                        textAlign: TextAlign.center,
                        overflow: TextOverflow.ellipsis,
                        style: const TextStyle(fontFamily: 'monospace', fontSize: 11, fontWeight: FontWeight.bold, color: Colors.amber),
                      ),
                    ),
                  ],
                ),
              ),
              const SizedBox(height: 10),
              ElevatedButton.icon(
                onPressed: _isCapturing ? null : _captureCurrentLocation,
                icon: const Icon(Icons.gps_fixed, size: 16),
                label: const Text("CAPTURE LIVE GPS PIN", style: TextStyle(fontSize: 12, fontWeight: FontWeight.bold)),
                style: ElevatedButton.styleFrom(
                  backgroundColor: const Color(0xFFCE1126),
                  foregroundColor: Colors.white,
                  padding: const EdgeInsets.symmetric(vertical: 10),
                ),
              ),
              const SizedBox(height: 8),
              ElevatedButton.icon(
                onPressed: _isSending ? null : _submitDataToServer,
                icon: const Icon(Icons.cloud_upload, size: 16),
                label: Text(_isSending ? "TRANSMITTING..." : "TRANSMIT PIN TO SERVER", style: const TextStyle(fontSize: 12, fontWeight: FontWeight.bold)),
                style: ElevatedButton.styleFrom(
                  backgroundColor: const Color(0xFF008751),
                  foregroundColor: Colors.white,
                  padding: const EdgeInsets.symmetric(vertical: 10),
                ),
              ),
              const SizedBox(height: 10),
              ClipRRect(
                borderRadius: BorderRadius.circular(6),
                child: Image.asset(
                  'assets/hero_bg.jpg',
                  height: 115,
                  fit: BoxFit.cover,
                ),
              ),
            ],
          ),
        ),
      ),
    );
  }
}