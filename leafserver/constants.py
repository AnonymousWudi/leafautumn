# coding=utf-8


class Enum(object):
    _enum_dict = {}

    def __init__(self, *args, **kwargs):
        self._enum_dict.update(
                dict(zip(args, xrange(len(args))), **kwargs)
        )

    def inv_dict(self):
        v = self._enum_dict.values()
        if len(v) != len(set(v)):
            raise "Cannont reverse key-value because the Enum obj has dulipcated values."
        return {v: k for k, v in self._enum_dict.iteritems()}

    def names(self):
        return self._enum_dict.keys()

    def values(self):
        return self._enum_dict.values()

    def get(self, key, default=None):
        return self._enum_dict.get(key, default)

    def __contains__(self, key):
        return key in self.values()

ERROR_DICT = {
    9002: u'ID对应对象不存在'  # 创建日期为2016-09-02 故为9002
}
