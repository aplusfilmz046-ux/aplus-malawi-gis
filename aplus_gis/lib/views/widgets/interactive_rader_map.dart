import 'package:flutter/material.dart';
import '../../theme.dart';

class InteractiveRadarMap extends StatelessWidget {
  const InteractiveRadarMap({super.key});

  @override
  Widget build(BuildContext context) {
    return Container(
      height: 380,
      decoration: BoxDecoration(
        color: AppColors.whiteSheet,
        borderRadius: BorderRadius.circular(20),
        boxShadow: [
          BoxShadow(color: Colors.black.withOpacity(0.05), blurRadius: 20, offset: const Offset(0, 4))
        ],
      ),
      child: Column(
        children: [
          Container(
            padding: const EdgeInsets.symmetric(horizontal: 20, vertical: 14),
            decoration: const BoxDecoration(border: Border(bottom: BorderSide(color: Colors.black12))),
            child: const Row(
              children: [
                Icon(Icons.map, color: AppColors.accentGreen, size: 18),
                SizedBox(width: 10),
                Text("Live Map Radar Workspace", style: TextStyle(fontWeight: FontWeight.bold, color: AppColors.textMainDark, fontSize: 14)),
                Spacer(),
                Icon(Icons.fullscreen, color: AppColors.textMutedDark, size: 18),
              ],
            ),
          ),
          Expanded(
            child: Container(
              decoration: const BoxDecoration(
                borderRadius: BorderRadius.only(bottomLeft: Radius.circular(20), bottomRight: Radius.circular(20)),
                color: Color(0xFF131C17),
              ),
              child: const Center(
                child: Column(
                  mainAxisAlignment: MainAxisAlignment.center,
                  children: [
                    Icon(Icons.radar, color: AppColors.accentGreen, size: 48),
                    SizedBox(height: 8),
                    Text("Malawi Address GIS Radar Active", style: TextStyle(color: Colors.white70, fontSize: 12, fontWeight: FontWeight.bold)),
                  ],
                ),
              ),
            ),
          )
        ],
      ),
    );
  }
}
