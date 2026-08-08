/// 4desk feature flags — Dart mirror of src/four_desk/feature_flags.rs.
/// Widgets only ever ask [FeatureFlags.isEnabled]; they never touch option
/// storage directly (Law of Demeter). Keys must match the Rust registry.
library;

/// Registry of all 4desk feature flags.
enum Flag {
  /// Demo flag: welcome banner for garage installs.
  garageWelcomeBanner(key: 'garage-welcome-banner', defaultEnabled: false);

  const Flag({required this.key, required this.defaultEnabled});

  /// Stable string key shared with the Rust registry.
  final String key;

  /// Compile-time default when no runtime override exists.
  final bool defaultEnabled;
}

/// Reads a raw override value ('Y' / 'N' / '') for a flag key.
/// Production wires this to the option storage bridge; tests inject a fake.
typedef OverrideReader = String Function(String optionName);

class FeatureFlags {
  FeatureFlags({required OverrideReader readOverride})
      : _readOverride = readOverride;

  static const optionPrefix = '4desk-flag-';

  final OverrideReader _readOverride;

  bool isEnabled(Flag flag) {
    switch (_readOverride('$optionPrefix${flag.key}')) {
      case 'Y':
        return true;
      case 'N':
        return false;
      default:
        return flag.defaultEnabled;
    }
  }
}
