

def _lustre_sort_suites_by_weight(lustre_testsuites):
    # attach weight
    cur_dict = dict.fromkeys(lustre_testsuites, 0)
    for suite in lustre_testsuites:
        if suite in lustre_suite_weight_dict.keys():
            cur_dict[suite] = lustre_suite_weight_dict[suite]
    sorted_list = sorted(cur_dict.iteritems(),
                         key=lambda d: d[1], reverse=True)
    sorted_suite_list = []
    del lustre_testsuites[:]
    for item in sorted_list:
        sorted_suite_list.append(item[1])

def lustre_sort_suites_by_weight(lustre_testsuites):
  #  l_func = lambda d:lustre_suite_weight_dict[d] if d in lustre_suite_weight_dict.keys() else 0
    def l_func(d):
        if d in lustre_suite_weight_dict.keys():
            return lustre_suite_weight_dict[d]
        else:
            return 0
    lustre_testsuites.sort(key=l_func, reverse=True)

lustre_default_test_suites = ["sanity", "sanityn", "mmp",
                              "sanity-scrub", "sanity-hsm", "sanity-lfsck",
                              "runtests", "lnet-selftest", "ost-pools",
                              "lustre-rsync-test", "sanity-sec", "sanity-quota",
                              "insanity", "replay-ost-single", "recovery-small",
                              "replay-single", "conf-sanity", "xxxxxx"]
lustre_suite_weight_dict = {'conf-sanity': 143, 'replay-dual': 92,
                            'replay-single': 81, 'replay-vbr': 81,
                            'sanity': 63, 'insanity': 56, 'sanity-scrub': 54,
                            'recovery-small': 52, 'sanity-hsm':51,
                            'sanity-lfsck': 32, 'sanityn': 32, 'sanity-quota': 32,
                            'replay-ost-single': 30, 'racer': 23, 'mmp': 22,
                            'ost-pools': 16, 'obdfilter-survey': 12, 'sanity-benchmark': 10,
                            'lustre-rsync-test': 9, 'lnet-selftest': 7, 'runtests': 6,
                            'metadata-updates':2, 'sanity-sec': 1, 'sgpdd-survey': 1, 'sanity-gss': 1}

print lustre_default_test_suites
lustre_sort_suites_by_weight(lustre_default_test_suites)

print lustre_default_test_suites

