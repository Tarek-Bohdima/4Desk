import 'package:flutter_hbb/four_desk/feature_flags.dart';
import 'package:flutter_test/flutter_test.dart';

void main() {
  FeatureFlags flagsWith(Map<String, String> stored) =>
      FeatureFlags(readOverride: (name) => stored[name] ?? '');

  group('FeatureFlags', () {
    test('default applies when no override stored', () {
      final flags = flagsWith({});
      expect(flags.isEnabled(Flag.garageWelcomeBanner),
          Flag.garageWelcomeBanner.defaultEnabled);
    });

    test('stored Y wins over default', () {
      final flags = flagsWith({'4desk-flag-garage-welcome-banner': 'Y'});
      expect(flags.isEnabled(Flag.garageWelcomeBanner), isTrue);
    });

    test('stored N wins over default', () {
      final flags = flagsWith({'4desk-flag-garage-welcome-banner': 'N'});
      expect(flags.isEnabled(Flag.garageWelcomeBanner), isFalse);
    });

    test('garbage override falls back to default', () {
      final flags = flagsWith({'4desk-flag-garage-welcome-banner': 'maybe'});
      expect(flags.isEnabled(Flag.garageWelcomeBanner),
          Flag.garageWelcomeBanner.defaultEnabled);
    });

    test('keys are prefixed and stable across the FFI boundary', () {
      expect(FeatureFlags.optionPrefix, '4desk-flag-');
      expect(Flag.garageWelcomeBanner.key, 'garage-welcome-banner');
    });
  });
}
