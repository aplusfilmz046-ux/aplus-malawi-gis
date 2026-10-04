import 'package:flutter/material.dart';
import '../../theme.dart';

class FunctionalSectorsGrid extends StatelessWidget {
  const FunctionalSectorsGrid({super.key});

  @override
  Widget build(BuildContext context) {
    final List<Map<String, String>> categories = [
      {"icon": "🏠", "title": "Homes", "desc": "Your family, safer, more connected", "img": "https://unsplash.com"},
      {"icon": "🏢", "title": "Businesses", "desc": "Grow your business with a real address", "img": "https://unsplash.com"},
      {"icon": "🌾", "title": "Farms", "desc": "Access support, markets & services", "img": "https://unsplash.com"},
      {"icon": "🎓", "title": "Schools", "desc": "Better planning and service delivery", "img": "https://unsplash.com"},
      {"icon": "⛪", "title": "Churches", "desc": "Reach your community more easily", "img": "https://unsplash.com"},
      {"icon": "🏥", "title": "Clinics & Hospitals", "desc": "Faster help, better care", "img": "https://unsplash.com"}
    ];

    return GridView.builder(
      shrinkWrap: true,
      physics: const NeverScrollableScrollPhysics(),
      gridDelegate: const SliverGridDelegateWithMaxCrossAxisExtent(
        maxCrossAxisExtent: 240,
        mainAxisSpacing: 16,
        crossAxisSpacing: 16,
        childAspectRatio: 0.85,
      ),
      itemCount: categories.length,
      itemBuilder: (context, idx) {
        final item = categories[idx];
        return Container(
          decoration: BoxDecoration(
            color: AppColors.whiteSheet,
            borderRadius: BorderRadius.circular(16),
            boxShadow: [
              BoxShadow(color: Colors.black.withOpacity(0.04), blurRadius: 10, offset: const Offset(0, 2))
            ],
          ),
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              Expanded(
                child: Container(
                  decoration: BoxDecoration(
                    borderRadius: const BorderRadius.only(topLeft: Radius.circular(16), topRight: Radius.circular(16)),
                    image: DecorationImage(image: NetworkImage(item['img']!), fit: BoxFit.cover),
                  ),
                ),
              ),
              Padding(
                padding: const EdgeInsets.all(12),
                child: Row(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    Text(item['icon']!, style: const TextStyle(fontSize: 20)),
                    const SizedBox(width: 8),
                    Expanded(
                      child: Column(
                        crossAxisAlignment: CrossAxisAlignment.start,
                        children: [
                          Text(item['title']!, style: const TextStyle(fontWeight: FontWeight.bold, fontSize: 13, color: AppColors.textMainDark)),
                          const SizedBox(height: 2),
                          Text(item['desc']!, style: const TextStyle(color: AppColors.textMutedDark, fontSize: 10, height: 1.2)),
                        ],
                      ),
                    )
                  ],
                ),
              )
            ],
          ),
        );
      },
    );
  }
}
