import ctypes


Py_ssize_t = ctypes.c_ssize_t
digit = ctypes.c_uint32


def starstar(type_):
    return ctypes.POINTER(ctypes.POINTER(type_))


def dereference(ptr):
    # ptr[0]
    # ptr.contents
    return ptr[0]


class PyObject(ctypes.Structure):
    _fields_ = [
        ("ob_refcnt", Py_ssize_t),  # Py_ssize_t ob_refcnt
        ("ob_type", ctypes.c_void_p),  # struct _typeobject *ob_type
    ]

    def __repr__(self):
        return f"PyObject(ob_refcnt={self.ob_refcnt}, ob_type={self.ob_type})"


class PyVarObject(ctypes.Structure):
    _fields_ = [
        ("ob_base", PyObject),  # PyObject ob_base
        ("ob_size", Py_ssize_t),  # Py_ssize_t ob_size
    ]

    def __repr__(self):
        return f"PyVarObject(ob_base={self.ob_base}, ob_size={self.ob_size})"


class _longobject(ctypes.Structure):
    _fields_ = [
        ("ob_base", PyVarObject),  # PyObject_VAR_HEAD
        ("ob_digit", digit * 1),  # digit ob_digit[1]
    ]

    def __repr__(self):
        return (
            "_longobject("
            f"ob_base={self.ob_base}, "
            f"ob_digit=[]{{{dereference(self.ob_digit)}}})"
        )


class PyListObject(ctypes.Structure):
    _fields_ = [
        ("ob_base", PyVarObject),  # PyObject_VAR_HEAD
        ("ob_item", starstar(PyObject)),  # PyObject **ob_item
        ("allocated", Py_ssize_t),  # Py_ssize_t allocated
    ]

    def __repr__(self):
        return (
            "PyListObject("
            # f"ob_refcnt={self.ob_base.ob_base.ob_refcnt}, "
            # f"ob_type={self.ob_base.ob_base.ob_type}, "
            # f"ob_size={self.ob_base.ob_size}, "
            f"ob_base={self.ob_base}, "
            f"ob_item={self.ob_item}, "
            f"allocated={self.allocated})"
        )


def explain_data(data):
    address = id(data)
    print(f"id(data)={address}")

    plo = PyListObject.from_address(address)
    print(plo)
    ptr_start = ctypes.addressof(dereference(plo.ob_item))
    print(f"ptr_start={ptr_start}")

    long_array_t = plo.ob_base.ob_size * ctypes.POINTER(_longobject)
    as_longs = long_array_t.from_address(ptr_start)
    for i in range(plo.ob_base.ob_size):
        # print(ctypes.addressof(as_longs[i]))
        print(dereference(as_longs[i]))


def main():
    data = [10001, 20001, 30002, 40003, 50005, 60008, 70013]
    explain_data(data)

    print("=" * 60)
    data.append(80021)
    explain_data(data)

    print("=" * 60)
    data.append(90034)
    explain_data(data)

    # print("=" * 60)
    # explain_data(data[1:])

    print("=" * 60)
    del data[0]
    explain_data(data)


if __name__ == "__main__":
    main()
