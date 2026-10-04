import 'package:flutter/material.dart';
import '../../theme.dart';

class BottomBrandingBar extends StatelessWidget {
  const BottomBrandingBar({super.key});

  @override
  Widget build(BuildContext context) {
    return Container(
      padding: const EdgeInsets.symmetric(vertical: 20, horizontal: 24),
      decoration: BoxDecoration(
        color: AppColors.sidebarBg,
        borderRadius: BorderRadius.circular(12),
        border: const Border(top: BorderSide(color: AppColors.accentRed, width: 2)),
      ),
      child: Row(
        mainAxisAlignment: MainAxisAlignment.spaceBetween,
        children: [
          Text(
            "© 2026 A+Malawi GIS Platform. Simple. Secure. For Everyone.",
            style: TextStyle(color: Colors.white.withOpacity(0.6), fontSize: 11),
          ),
          Text(
            "Together we build a better Malawi 🇲🇼",
            style: TextStyle(color: Colors.white.withOpacity(0.8), fontSize: 11, fontWeight: FontWeight.bold),
          ),
        ],
      ),
    );
  }
}
