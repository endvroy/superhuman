import instructions

class hrm(object):
    def __init__(self, initial_st, insts, fp=0):
        self.initial_st = initial_st
        self.st = initial_st
        self.insts = insts
        self.fp = fp

    def exec_n(self, n):
        i = 0
        while i < n and self.fp < len(self.insts):
            self._exec()
        return self.st

    def run(self):
        while self.fp < len(self.insts):
            self._exec()
        return self.st

    def _exec(self):
        if self.fp == len(self.insts):
            return None

        (inst, args) = self.insts[self.fp]
        if inst == instructions.jump:
            self.fp = args[0]
        elif inst == instructions.jumpIfZero:
            if st.reg.is_empty():
                raise ValueError('invalid read on null reg')
            elif st.reg.val == 0:
                self.fp = args[0]
        elif inst == instructions.jumpIfNegative:
            if st.reg.is_empty():
                raise ValueError('invalid read on null reg')
            elif st.reg.val < 0:
                self.fp = args[0]
        else:
            # normal instructions
            args = self.st + args
            self.st = inst(*args)

        # increment fp
        self.fp += 1
        return self.st
