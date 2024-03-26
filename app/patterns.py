
pattern_1 = "-----------beginning of crash" \
            "terminationReason: (none)" \
            "AndroidRuntime: Process: com.google.android.googlequicksearchbox:search"
pattern_2 = "ActivityManager: ANR"
pattern_3 = "EXC_CRASHSIGABRT" \
            "java.lang.IllegalStateException"
pattern_4 = "IPCThreadState: Calling IPCThreadState::self() during shutdown is dangerous, expect a crash."

patterns_set = {pattern_1, pattern_2, pattern_3, pattern_4}
