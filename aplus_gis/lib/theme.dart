import 'package:flutter/material.dart';

class AppColors {
  // Deep charcoal background matching your primary dashboard container frame
  static const Color sidebarBg = Color(0xFF0A0F0B);

  // Vivid Malawi Flag Red for high-action registration buttons and indicators
  static const Color accentRed = Color(0xFFCE1126);

  // Vibrant Flag Green for success status capsules and active tab links
  static const Color accentGreen = Color(0xFF008751);

  // High-contrast deep tones for sharp readable typography
  static const Color textMainDark = Color(0xFF111111);
  static const Color textMutedDark = Color(0xFF666666);

  // Clean secondary background canvas sheet color
  static const Color backgroundLight = Color(0xFFF4F6F8);
  static const Color whiteSheet = Color(0xFFFFFFFF);

  // Premium glassmorphism gradients for your background hero stage block
  static const LinearGradient heroGradient = LinearGradient(
    colors: [Color(0xFF070F0B), Color(0xFF131C17)],
    begin: Alignment.topLeft,
    end: Alignment.bottomRight,
  );

  // Gradient track for buttons and walkthrough highlights
  static const LinearGradient registrationGradient = LinearGradient(
    colors: [Color(0xFF008751), Color(0xFF005A32)],
    begin: Alignment.centerLeft,
    end: Alignment.centerRight,
  );

  // Custom container gradient for testimonial cards
  static const LinearGradient quoteGradient = LinearGradient(
    colors: [Color(0xFF0B1511), Color(0xFF1A2E26)],
    begin: Alignment.topLeft,
    end: Alignment.bottomRight,
  );
}
