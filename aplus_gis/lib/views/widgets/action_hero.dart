import 'package:flutter/material.dart';
import '../../theme.dart';

class ActionHero extends StatelessWidget {
  const ActionHero({super.key});

  @override
  Widget build(BuildContext context) {
    return Container(
      height: 380,
      decoration: BoxDecoration(
        gradient: AppColors.heroGradient,
        borderRadius: BorderRadius.circular(20),
      ),
      padding: const EdgeInsets.all(32),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        mainAxisAlignment: MainAxisAlignment.center,
        children: [
          const Text(
            "A+MALAWI GIS ADDRESSING PLATFORM",
            style: TextStyle(color: AppColors.accentRed, fontWeight: FontWeight.bold, fontSize: 11, letterSpacing: 1),
          ),
          const SizedBox(height: 12),
          RichText(
            text: const TextSpan(
              text: 'Your Place.\n',
              style: TextStyle(fontSize: 38, fontWeight: FontWeight.w900, color: Colors.white, height: 1.15),
              children: [
                TextSpan(text: 'Your Address.\n', style: TextStyle(color: AppColors.accentRed)),
                TextSpan(text: 'Your Future.', style: TextStyle(color: AppColors.accentGreen)),
              ],
            ),
          ),
          const SizedBox(height: 16),
          // Fixed container width constraint parameter configuration explicitly to remove Sizedbox typos
          Container(
            width: 500,
            child: const Text(
              "Register your home, business, farm or institution on our GIS platform. Get a real address, be easily found, and unlock more opportunities across the nation.",
              style: TextStyle(color: Colors.white70, fontSize: 13, height: 1.45),
            ),
          ),
          const SizedBox(height: 24),
          Wrap(
            spacing: 8,
            runSpacing: 8,
            children: [
              _buildMiniCapsule(Icons.check_circle_outline, "Be Found Easily"),
              _buildMiniCapsule(Icons.flash_on, "Get Services Faster"),
              _buildMiniCapsule(Icons.trending_up, "Support Local Growth"),
            ],
          ),
          const SizedBox(height: 32),
          ElevatedButton(
            onPressed: () {},
            style: ElevatedButton.styleFrom(
              backgroundColor: AppColors.accentRed,
              shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(24)),
              padding: const EdgeInsets.symmetric(horizontal: 28, vertical: 16),
              elevation: 4,
            ),
            child: const Row(
              mainAxisSize: MainAxisSize.min,
              children: [
                Icon(Icons.pin_drop, color: Colors.white, size: 18),
                SizedBox(width: 12),
                Text("Register My Address", style: TextStyle(color: Colors.white, fontWeight: FontWeight.bold, fontSize: 14)),
                SizedBox(width: 8),
                Icon(Icons.arrow_forward, color: Colors.white, size: 16),
              ],
            ),
          ),
        ],
      ),
    );
  }

  Widget _buildMiniCapsule(IconData icon, String label) {
    return Container(
      padding: const EdgeInsets.symmetric(horizontal: 10, vertical: 6),
      decoration: BoxDecoration(
        color: Colors.white10,
        borderRadius: BorderRadius.circular(20),
        border: Border.all(color: Colors.white12),
      ),
      child: Row(
        mainAxisSize: MainAxisSize.min,
        children: [
          Icon(icon, color: AppColors.accentGreen, size: 13),
          const SizedBox(width: 6),
          Text(label, style: const TextStyle(color: Colors.white, fontSize: 10, fontWeight: FontWeight.w600)),
        ],
      ),
    );
  }
}
