import { NativeModules, Platform } from 'react-native';

export type SdkEnvironmentName = 'production' | 'development';

export type BoltEarthUiSdkInitConfig = {
  userId: string;
  sdkToken: string;
  environment?: SdkEnvironmentName;
  primaryColor: string;
  localeLanguageTag: string;
};

type NativeBoltEarthUiSdkRn = {
  initialize(
    userId: string,
    sdkToken: string,
    environment: SdkEnvironmentName,
    primaryColor: string,
    localeLanguageTag: string,
  ): Promise<void>;
  openChargerBookingFlow(): Promise<void>;
};

const Native = NativeModules.BoltEarthUiSdkRn as NativeBoltEarthUiSdkRn | undefined;

function ensureAndroid(): void {
  if (Platform.OS !== 'android') {
    throw new Error('react-native-bolt-earth-ui-sdk is only implemented on Android.');
  }
  if (!Native) {
    throw new Error(
      'BoltEarthUiSdkRn native module is missing. Did you add BoltEarthUiSdkReactNativePackage to MainApplication and rebuild?',
    );
  }
}

/**
 * Mirrors `BoltEarthUiSdk.initialize(...)`.
 * Runs on the Android main thread inside the native module.
 */
export async function initialize(config: BoltEarthUiSdkInitConfig): Promise<void> {
  ensureAndroid();
  const env = config.environment ?? 'production';
  await Native!.initialize(
    config.userId,
    config.sdkToken,
    env,
    config.primaryColor,
    config.localeLanguageTag,
  );
}

/**
 * Mirrors `BoltEarthUiSdk.openChargerBookingFlow(activity)` using the current RN Activity.
 */
export async function openChargerBookingFlow(): Promise<void> {
  ensureAndroid();
  await Native!.openChargerBookingFlow();
}
