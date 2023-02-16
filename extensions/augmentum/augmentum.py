R"%%%(
import re
import abc

class Value:
    def __init__(self, address, size):
        if address is None:
            assert size is not None
            self.alloc = impl.Allocation(size)
            self._address = self.alloc.address
        else:
            self._address = address;
    
    @property
    @abc.abstractmethod
    def type_desc(self):
        pass
    
    @property
    def address(self):
        return self._address

    def __eq__(self, other):
        if isinstance(other, Value):
            return self._address == other._address
        return False

    def __repr__(self):
        return f"<augmentum.Value address {hex(self._address)}>"

class I32(Value):
    def __init__(self, value = None, address = None):
        super().__init__(address, 4)
        if value is not None:
            self.value = value
    
    @property
    def type_desc(self):
        return impl.i32_type()

    @property
    def value(self):
        return impl.i32_get(self._address)
    
    @value.setter
    def value(self, v):
        impl.i32_set(self._address, v)
        
    def __str__(self):
        return str(self.value)

    def __repr__(self):
        return f"<augmentum.I32Value address {hex(self._address)} value {self.value}>"


class TypeDesc(abc.ABC):    
    @property
    @abc.abstractmethod
    def signature(self):
        pass

    @property
    def ptr(self):
        return impl.ptr_type()

    def __eq__(self, other):
        if isinstance(other, str):
            return self.signature == other
        return self.signature == other.signature
    
    def __str__(self):
        return self.signature


class UnknownTypeDesc(TypeDesc):
    def __init__(self, signature):
        self.signature = signature

    @property
    def signature(self):
        return self.signature

    def __repr__(self):
        return f"<augmentum.UnknownTypeDesc signature '{self.signature}'>"


class VoidTypeDesc(TypeDesc):
    @property
    def signature(self):
         return "void"

    def __repr__(self):
        return f"<augmentum.VoidTypeDesc>"


class IntTypeDesc(TypeDesc):
    @property
    def signature(self):
         return "void"

    def __repr__(self):
        return f"<augmentum.VoidTypeDesc>"


class FnTypeDesc(TypeDesc):
    def __init__(self, signature, return_type, arg_types):
        super().__init__(signature)
        self._return_type = return_type
        self._arg_types = arg_types

    @property
    def return_type(self):
        return self._return_type
    
    @property
    def arg_types(self):
        return self._arg_types

    def __repr__(self):
        return f"<augmentum.FnTypeDesc signature '{self.signature}'>"


class FnExtensionPoint:
    def __init__(self, module_name, name, ftype):
        self._module_name = module_name
        self._name = name
        self._type = ftype
    
    @property
    def name(self):
        return self._name

    @property
    def module_name(self):
        return self._module_name

    @property
    def ftype(self):
        return self._ftype
    
    @property
    def signature(self):
        return self._ftype.signature
    
    @property
    def return_type(self):
        return self._type.return_type
    
    @property
    def arg_types(self):
        return self._type.arg_types
    
    @property
    def signature(self):
        return self._type.signature
    
    def extend_before(self, advice, id = 0):
        impl.extend_before(self, advice, id)

    def extend_around(self, advice, id = 0):
        impl.extend_around(self, advice, id)

    def extend_after(self, advice, id = 0):
        impl.extend_after(self, advice, id)

    def remove(self, id):
        assert(id != 0)
        impl.remove(self, id)    

    def call_previous(self, handle, ret_val, *args):
        impl.call_previous(self, handle, ret_val, args)
        return ret_val
    
    def __eq__(self, other):
        if isinstance(other, str):
            return self.name == other
        return self.name == other.name

    def __str__(self):
        return self.name

    def __repr__(self):
        return f"<augmentum.FnExtensionPoint name '{self.name}'>"


class Listener:
    def __init__(self):
        impl.add_listener(self)

    def on_extension_point_register(self, pt):
        pass

    def on_extension_point_unregister(self, pt):
        pass

    @property
    def unique_advice_id(self):
        return impl.get_unique_advice_id()


class _SimpleListener(Listener):
    def __init__(self, which, advice, pt_pred, module_name_pred, name_pred, signature_pred):
        self.id = self.unique_advice_id
        self.which = which
        self.advice = advice
        self.pt_pred = pt_pred
        self.module_name_pred = module_name_pred
        self.name_pred = name_pred
        self.signature_pred = signature_pred
        super().__init__()

    def _check_str(self, string, pred):
        """Check a string against a predicate"""
        if pred is None:
            return True
        if callable(pred):
            return pred(string)
        if isinstance(pred, str):
            return pred == string
        if isinstance(pred, re.Pattern):
            return bool(pred.match(string))
        return False
        
    def _match(self, pt):
        if self.pt_pred is not None:
            if not self.pt_pred(pt):
                return False
        if not self._check_str(pt.module_name, self.module_name_pred):
            return False
        if not self._check_str(pt.name, self.name_pred):
            return False
        if not self._check_str(pt.signature, self.signature_pred):
            return False
        return True

    def on_extension_point_register(self, pt):
        if self._match(pt):
            extend = getattr(pt, "extend_" + self.which)
            extend(self.advice, self.id)

    def on_extension_point_unregister(self, pt):
        if self._match(pt):
            pt.remove(self.id)
    
    
def extend_before(advice, pt_pred = None, module_name_pred = None, name_pred = None, signature_pred = None):
    return _SimpleListener("before", advice, pt_pred, module_name_pred, name_pred, signature_pred)

def extend_around(advice, pt_pred = None, module_name_pred = None, name_pred = None, signature_pred = None):
    return _SimpleListener("around", advice, pt_pred, module_name_pred, name_pred, signature_pred)

def extend_after(advice, pt_pred = None, module_name_pred = None, name_pred = None, signature_pred = None):
    return _SimpleListener("after", advice, pt_pred, module_name_pred, name_pred, signature_pred)

)%%%";