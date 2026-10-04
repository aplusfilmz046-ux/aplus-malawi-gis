import 'package:flutter/material.dart';
import '../../theme.dart';

class TestialmonialQuoteCard extends StatelessWidget {
  const TestialmonialQuoteCard({super.key});

  @override
  Widget build(BuildContext context) {
    return Container(
      padding: const EdgeInsets.all(24),
      decoration: BoxDecoration(
        gradient: AppColors.quoteGradient,
        borderRadius: BorderRadius.circular(16),
      ),
      child: const Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        mainAxisAlignment: MainAxisAlignment.center,
        children: [
          Icon(Icons.format_quote, color: AppColors.accentGreen, size: 36),
          SizedBox(height: 12),
          Text(
            "\"With a real address, I got deliveries, customers and new opportunities. It changed my life!\"",
            style: TextStyle(color: Colors.white, fontSize: 13, fontStyle: FontStyle.italic, height: 1.45),
          ),
          SizedBox(height: 16),
          Text("— Grace M., Blantyre", style: TextStyle(color: Colors.white70, fontSize: 11, fontWeight: FontWeight.bold)),
        ],
      ),
    );
  }
}
