import 'package:flutter/material.dart';
import '../../theme.dart';

class PipelineWalkthrough extends StatelessWidget {
  const PipelineWalkthrough({super.key});

  @override
  Widget build(BuildContext context) {
    return Container(
      padding: const EdgeInsets.all(24),
      decoration: BoxDecoration(
        color: const Color(0xFF0F1712),
        borderRadius: BorderRadius.circular(16),
      ),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          const Text("Get Your Address in", style: TextStyle(color: Colors.white70, fontSize: 13)),
          const Text("3 Easy Steps", style: TextStyle(fontWeight: FontWeight.w900, color: Colors.white, fontSize: 24)),
          const SizedBox(height: 24),
          _buildPipelineRow("1", "Locate", "Your Place"),
          _buildDividerLine(),
          _buildPipelineRow("2", "Register", "Your Details"),
          _buildDividerLine(),
          _buildPipelineRow("3", "Get Verified", "& Share"),
          const SizedBox(height: 24),
          SizedBox(
            width: double.infinity,
            child: ElevatedButton(
              onPressed: () {},
              style: ElevatedButton.styleFrom(
                backgroundColor: AppColors.accentGreen,
                shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(20)),
                padding: const EdgeInsets.symmetric(vertical: 14),
              ),
              child: const Text("Start Registration →", style: TextStyle(color: Colors.white, fontWeight: FontWeight.bold)),
            ),
          )
        ],
      ),
    );
  }

  Widget _buildPipelineRow(String num, String heading, String trailing) {
    return Row(
      children: [
        CircleAvatar(
            radius: 14,
            backgroundColor: Colors.white,
            child: Text(num, style: const TextStyle(color: AppColors.sidebarBg, fontWeight: FontWeight.bold, fontSize: 13))
        ),
        const SizedBox(width: 16),
        Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Text(heading, style: const TextStyle(color: Colors.white, fontWeight: FontWeight.bold, fontSize: 14)),
            Text(trailing, style: const TextStyle(color: Colors.white60, fontSize: 12)),
          ],
        )
      ],
    );
  }

  Widget _buildDividerLine() {
    return Container(
      margin: const EdgeInsets.only(left: 14, top: 4, bottom: 4),
      width: 2,
      height: 20,
      color: Colors.white24,
    );
  }
}
