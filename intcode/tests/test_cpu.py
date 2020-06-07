import unittest
import intcode

class TestCpu(unittest.TestCase):

    def test_exit_op(self):
        simple_cpu = intcode.Cpu([99,])
        self.assertEqual(simple_cpu.run(), (0,))

    def test_add(self):
        code = [1, 0, 0, 0, 99]
        addition = intcode.Cpu(code)
        addition.run()
        result = addition.read(0)
        self.assertEqual(result, 2)

    def test_mult(self):
        code = [2, 4, 4, 5, 99, 0]
        vm = intcode.Cpu(code)
        vm.run()
        result = vm.read(5)
        self.assertEqual(result, 9801)

    def test_input_halt(self):
        code = [3, 50, 99]
        vm = intcode.Cpu(code)
        result = vm.run()
        self.assertEqual(result, (1, ))

    def test_input(self):
        code = [3, 50, 99]
        vm = intcode.Cpu(code)
        vm.run()
        vm.input(33)
        vm.run()
        result = vm.read(50)
        self.assertEqual(result, 33)

    def test_input_buffer(self):
        code = [3, 50, 99]
        vm = intcode.Cpu(code)
        vm.input(76)
        vm.run()
        result = vm.read(50)
        self.assertEqual(result, 76)

    def test_output(self):
        code = [4, 6, 99, 0, 0, 0, 43]
        vm = intcode.Cpu(code)
        rc, result = vm.run()
        self.assertEqual(rc, 2)
        self.assertEqual(result, 43)

    def test_eq_position(self):
        code = [3, 9, 8, 9, 10, 9, 4, 9, 99, -1, 8]
        vm = intcode.Cpu(code)
        vm.input(8)
        rc, result = vm.run()
        self.assertEqual(rc, 2)
        self.assertEqual(result, 1)

    def test_lt_position(self):
        code = [3,9,7,9,10,9,4,9,99,-1,8]
        vm = intcode.Cpu(code)
        vm.input(4)
        rc, result = vm.run()
        self.assertEqual(rc, 2)
        self.assertEqual(result, 1)

    def test_eq_immediate(self):
        code = [3,3,1108,-1,8,3,4,3,99]
        vm = intcode.Cpu(code)
        vm.input(8)
        rc, result = vm.run()
        self.assertEqual(rc, 2)
        self.assertEqual(result, 1)

    def test_lt_immediate(self):
        code = [3,3,1107,-1,8,3,4,3,99]
        vm = intcode.Cpu(code)
        vm.input(4)
        rc, result = vm.run()
        self.assertEqual(rc, 2)
        self.assertEqual(result, 1)

    def test_jmp_position(self):
        code = [3,12,6,12,15,1,13,14,13,4,13,99,-1,0,1,9]
        vm = intcode.Cpu(code)
        vm.input(33)
        rc, result = vm.run()
        self.assertEqual(rc, 2)
        self.assertEqual(result, 1)

    def test_jmp_immediate(self):
        code = [3,3,1105,-1,9,1101,0,0,12,4,12,99,1]
        vm = intcode.Cpu(code)
        vm.input(33)
        rc, result = vm.run()
        self.assertEqual(rc, 2)
        self.assertEqual(result, 1)

    def test_relative(self):
        code = [109, 5, 204, 2, 99, -1, -1, 15]
        vm = intcode.Cpu(code)
        rc, result = vm.run()
        self.assertEqual(rc, 2)
        self.assertEqual(result, 15)

if __name__ == '__main__':
    unittest.main()

