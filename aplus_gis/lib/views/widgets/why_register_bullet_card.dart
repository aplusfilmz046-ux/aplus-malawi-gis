import 'package:flutter/material.dart';
import '../../theme.dart';

class WhyRegisterBulletCard extends StatelessWidget {
  const WhyRegisterBulletCard({super.key});

  @override
  Widget build(BuildContext context) {
    return Container(
      padding: const EdgeInsets.all(24),
      decoration: BoxDecoration(
        color: AppColors.whiteSheet,
        borderRadius: BorderRadius.circular(16),
        boxShadow: [
          BoxShadow(color: Colors.black.withOpacity(0.03), blurRadius: 10)
        ],
      ),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          const Text("Why Register?", style: TextStyle(fontWeight: FontWeight.bold, color: AppColors.textMainDark, fontSize: 18)),
          const SizedBox(height: 16),
          _buildBulletItem("Access decentralized government services seamlessly"),
          _buildBulletItem("Receive ecommerce deliveries & online shopping directly"),
          _buildBulletItem("Emergency medical services can find your plot instantly"),
          _buildBulletItem("Grow your business location visibility on rideshare routing maps"),
          _buildBulletItem("Acquire highly accurate positioning tokens from your location safely"),
        ],
      ),
    );
  }

  Widget _buildBulletItem(String text) {
    return Padding(
      padding: const EdgeInsets.only(bottom: 12.0),
      child: Row(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          const Icon(Icons.check, color: AppColors.accentGreen, size: 16),
          const SizedBox(width: 12),
          Expanded(child: Text(text, style: const TextStyle(color: AppColors.textMutedDark, fontSize: 13, height: 1.3))),
        ],
      ),
    );
  }
}
