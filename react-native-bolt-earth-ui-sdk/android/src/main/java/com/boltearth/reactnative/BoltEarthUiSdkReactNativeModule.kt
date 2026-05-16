package com.boltearth.reactnative

import android.os.Handler
import android.os.Looper
import com.boltearthsdk.BoltEarthUiSdk
import com.boltearthsdk.SdkEnvironment
import com.boltearthsdk.SdkFontOverrides
import com.facebook.react.bridge.Promise
import com.facebook.react.bridge.ReactApplicationContext
import com.facebook.react.bridge.ReactContextBaseJavaModule
import com.facebook.react.bridge.ReactMethod

class BoltEarthUiSdkReactNativeModule(reactContext: ReactApplicationContext) :
    ReactContextBaseJavaModule(reactContext) {

    private val mainHandler = Handler(Looper.getMainLooper())

    override fun getName(): String = "BoltEarthUiSdkRn"

    @ReactMethod
    fun initialize(
        userId: String,
        sdkToken: String,
        environment: String,
        primaryColor: String,
        localeLanguageTag: String,
        promise: Promise,
    ) {
        mainHandler.post {
            try {
                val env =
                    when (environment.lowercase()) {
                        "production" -> SdkEnvironment.Production
                        else -> SdkEnvironment.Development
                    }
                BoltEarthUiSdk.initialize(
                    reactApplicationContext.applicationContext,
                    userId,
                    sdkToken,
                    env,
                    primaryColor,
                    SdkFontOverrides(),
                    localeLanguageTag,
                )
                promise.resolve(null)
            } catch (e: Exception) {
                promise.reject("BOLT_EARTH_INIT_ERROR", e.message, e)
            }
        }
    }

    @ReactMethod
    fun openChargerBookingFlow(promise: Promise) {
        val activity = currentActivity
        if (activity == null) {
            promise.reject("BOLT_EARTH_NO_ACTIVITY", "No React Native Activity is available.")
            return
        }
        activity.runOnUiThread {
            try {
                BoltEarthUiSdk.openChargerBookingFlow(activity)
                promise.resolve(null)
            } catch (e: Exception) {
                promise.reject("BOLT_EARTH_FLOW_ERROR", e.message, e)
            }
        }
    }
}
