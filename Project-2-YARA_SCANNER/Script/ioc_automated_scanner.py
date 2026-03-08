import hashlib


class Exteact_ioc:
 
    def Get_Hash(self, path, alg="sha256"):

        hash_func = getattr(hashlib, alg)
        fun = hash_func()

        with open(path, "rb") as f:
            while chunk := f.read(4096):
                fun.update(chunk)

        return fun.hexdigest()
    