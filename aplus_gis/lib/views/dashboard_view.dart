import 'package:flutter/material.dart';
import '../theme.dart';
import 'widgets/action_hero.dart';
import 'widgets/functional_sectors_grid.dart';
import 'widgets/pipeline_walkthrough.dart';
import 'widgets/why_register_bullet_card.dart';
import 'widgets/testimonial_quote_card.dart';
import 'widgets/bottom_branding_bar.dart';
import 'widgets/interactive_radar_map.dart'; // Safely linked via its own independent file structure

class DashboardView extends StatefulWidget {
  const DashboardView({super.key});

  @override
  State<DashboardView> createState() => _DashboardViewState();
}

class _DashboardViewState extends State<DashboardView> {
  final GlobalKey<ScaffoldState> _scaffoldKey = GlobalKey<ScaffoldState>();
  final TextEditingController _searchController = TextEditingController();
  String _activeTab = 'Home';

  Widget _buildSidebarNavItem(IconData icon, String title) {
    final bool isActive = _activeTab == title;
    return Padding(
      padding: const EdgeInsets.only(bottom: 8.0),
      child: InkWell(
        onTap: () {
          setState(() { _activeTab = title; });
          if (MediaQuery.of(context).size.width <= 900) { Navigator.pop(context); }
        },
        borderRadius: BorderRadius.circular(8),
        child: Container(
          padding: const EdgeInsets.symmetric(vertical: 12, horizontal: 16),
          decoration: BoxDecoration(
            color: isActive ? AppColors.accentGreen : Colors.transparent,
            borderRadius: BorderRadius.circular(8),
          ),
          child: Row(
            children: [
              Icon(icon, color: isActive ? Colors.white : Colors.white70, size: 20),
              const SizedBox(width: 16),
              Text(title, style: TextStyle(color: isActive ? Colors.white : Colors.white70, fontWeight: isActive ? FontWeight.bold : FontWeight.normal, fontSize: 14)),
            ],
          ),
        ),
      ),
    );
  }

  Widget _buildSidebar(BuildContext context) {
    return Container(
      width: 260, height: double.infinity, color: AppColors.sidebarBg,
      padding: const EdgeInsets.symmetric(vertical: 24, horizontal: 16),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Row(
            children: [
              Container(
                width: 36, height: 36,
                decoration: const BoxDecoration(gradient: RadialGradient(colors: [AppColors.accentRed, AppColors.sidebarBg]), shape: BoxShape.circle),
              ),
              const SizedBox(width: 12),
              Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  RichText(
                    text: const TextSpan(
                      text: 'A+', style: TextStyle(fontWeight: FontWeight.w900, fontSize: 20, color: AppColors.accentRed),
                      children: [TextSpan(text: 'Malawi', style: TextStyle(color: Colors.white))],
                    ),
                  ),
                  const Text("GIS ADDRESSING PLATFORM", style: TextStyle(color: Colors.white60, fontSize: 8, fontWeight: FontWeight.bold, letterSpacing: 0.5)),
                ],
              )
            ],
          ),
          const SizedBox(height: 32),
          Expanded(
            child: Column(
              children: [
                _buildSidebarNavItem(Icons.home, "Home"),
                _buildSidebarNavItem(Icons.pin_drop, "Register Address"),
                _buildSidebarNavItem(Icons.search, "Find Address"),
                _buildSidebarNavItem(Icons.map, "Map View"),
                _buildSidebarNavItem(Icons.folder_shared, "My Addresses"),
                _buildSidebarNavItem(Icons.layers, "Services"),
                _buildSidebarNavItem(Icons.info, "About"),
                _buildSidebarNavItem(Icons.help_center, "Help & Support"),
              ],
            ),
          ),
          const Divider(color: Colors.white24),
          const SizedBox(height: 8),
          const Center(child: Text("One Malawi • One Address", style: TextStyle(color: AppColors.accentRed, fontStyle: FontStyle.italic, fontSize: 12, fontWeight: FontWeight.bold)))
        ],
      ),
    );
  }

  @override
  Widget build(BuildContext context) {
    final bool isDesktop = MediaQuery.of(context).size.width > 900;

    return Scaffold(
      key: _scaffoldKey, backgroundColor: AppColors.backgroundLight,
      drawer: !isDesktop ? _buildSidebar(context) : null,
      appBar: !isDesktop
          ? AppBar(
        backgroundColor: AppColors.sidebarBg, elevation: 0,
        leading: IconButton(icon: const Icon(Icons.menu, color: Colors.white), onPressed: () => _scaffoldKey.currentState?.openDrawer()),
        title: const Text("A+Malawi GIS", style: TextStyle(fontWeight: FontWeight.w900, color: Colors.white)),
      )
          : null,
      body: Row(
        children: [
          if (isDesktop) _buildSidebar(context),
          Expanded(
            child: Column(
              children: [
                Container(
                  color: AppColors.whiteSheet, padding: const EdgeInsets.symmetric(horizontal: 24, vertical: 16),
                  child: Row(
                    children: [
                      Expanded(
                        child: Container(
                          height: 44, decoration: BoxDecoration(color: AppColors.backgroundLight, borderRadius: BorderRadius.circular(22), border: Border.all(color: Colors.black12)),
                          padding: const EdgeInsets.only(left: 16, right: 6),
                          child: Row(
                            children: [
                              const Icon(Icons.search, color: AppColors.textMutedDark, size: 20),
                              const SizedBox(width: 12),
                              Expanded(child: TextField(controller: _searchController, decoration: const InputDecoration(hintText: 'Search for a place, address or location...', border: InputBorder.none, isDense: true, hintStyle: TextStyle(color: AppColors.textMutedDark, fontSize: 13)))),
                              ElevatedButton(onPressed: () {}, style: ElevatedButton.styleFrom(backgroundColor: AppColors.accentGreen), child: const Text("Search", style: TextStyle(color: Colors.white))),
                            ],
                          ),
                        ),
                      ),
                      const SizedBox(width: 16),
                      const CircleAvatar(radius: 18, backgroundColor: AppColors.backgroundLight, child: Icon(Icons.person, color: AppColors.textMainDark)),
                    ],
                  ),
                ),
                Expanded(
                  child: ListView(
                    padding: const EdgeInsets.symmetric(horizontal: 24, vertical: 20),
                    children: [
                      Row(
                        crossAxisAlignment: CrossAxisAlignment.start,
                        children: [
                          const Expanded(flex: 3, child: ActionHero()),
                          const SizedBox(width: 24),
                          Expanded(flex: 2, child: InteractiveRadarMap()),
                        ],
                      ),
                      const SizedBox(height: 32),
                      const FunctionalSectorsGrid(),
                      const SizedBox(height: 32),
                      Row(
                        crossAxisAlignment: CrossAxisAlignment.start,
                        children: [
                          const Expanded(flex: 3, child: PipelineWalkthrough()),
                          const SizedBox(width: 24),
                          const Expanded(flex: 3, child: WhyRegisterBulletCard()),
                          const SizedBox(width: 24),
                          Expanded(flex: 2, child: const TestialmonialQuoteCard()),
                        ],
                      ),
                      const SizedBox(height: 40),
                      const BottomBrandingBar(),
                    ],
                  ),
                ),
              ],
            ),
          ),
        ],
      ),
    );
  }
}
