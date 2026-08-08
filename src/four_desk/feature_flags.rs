//! 4desk feature flags: single entry point for enabling/disabling 4desk
//! features on every platform.
//!
//! Resolution order (first match wins):
//! 1. Runtime override stored in local options as `4desk-flag-<key>` = "Y"/"N"
//!    (settable per install; later a server-pushed config can write these).
//! 2. Compile-time default from the registry below.
//!
//! Callers only ever ask `is_enabled(flag)` — never dig into config storage.

use hbb_common::config::LocalConfig;

/// Registry of all 4desk feature flags. Add new features here (one line)
/// and document them in docs/how-to/add-a-feature-flag.md.
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum Flag {
    /// Demo flag: welcome banner for garage installs.
    GarageWelcomeBanner,
}

impl Flag {
    /// Stable string key; must match the Dart registry
    /// (flutter/lib/four_desk/feature_flags.dart).
    pub fn key(&self) -> &'static str {
        match self {
            Flag::GarageWelcomeBanner => "garage-welcome-banner",
        }
    }

    /// Compile-time default when no runtime override exists.
    pub fn default_enabled(&self) -> bool {
        match self {
            Flag::GarageWelcomeBanner => false,
        }
    }
}

const OPTION_PREFIX: &str = "4desk-flag-";

/// Whether a 4desk feature is enabled on this install.
pub fn is_enabled(flag: Flag) -> bool {
    resolve(flag, &LocalConfig::get_option(&option_name(flag)))
}

/// Set or clear (empty string) the runtime override for a flag.
pub fn set_override(flag: Flag, enabled: Option<bool>) {
    let value = match enabled {
        Some(true) => "Y",
        Some(false) => "N",
        None => "",
    };
    LocalConfig::set_option(option_name(flag), value.to_owned());
}

fn option_name(flag: Flag) -> String {
    format!("{}{}", OPTION_PREFIX, flag.key())
}

fn resolve(flag: Flag, stored: &str) -> bool {
    match stored {
        "Y" => true,
        "N" => false,
        _ => flag.default_enabled(),
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn default_applies_when_no_override_stored() {
        assert_eq!(
            resolve(Flag::GarageWelcomeBanner, ""),
            Flag::GarageWelcomeBanner.default_enabled()
        );
    }

    #[test]
    fn stored_yes_wins_over_default() {
        assert!(resolve(Flag::GarageWelcomeBanner, "Y"));
    }

    #[test]
    fn stored_no_wins_over_default() {
        assert!(!resolve(Flag::GarageWelcomeBanner, "N"));
    }

    #[test]
    fn garbage_override_falls_back_to_default() {
        assert_eq!(
            resolve(Flag::GarageWelcomeBanner, "maybe"),
            Flag::GarageWelcomeBanner.default_enabled()
        );
    }

    #[test]
    fn option_name_is_prefixed_stable_key() {
        assert_eq!(
            option_name(Flag::GarageWelcomeBanner),
            "4desk-flag-garage-welcome-banner"
        );
    }
}
