#lang s-exp rosette/safe

(require racket/list)

(struct state (reg mem output) #:transparent)

; exec one instr
(define (exec instr st)
  (let ([opcode (first instr)]
        [operands (append (rest instr) (list st))])
    (apply opcode operands)))

; interpret seq of instr
(define (interpret instr-list st)
  (if (empty? instr-list)
      st
      (let ([instr (first instr-list)])
        (define new-st (exec instr st))
        (interpret (rest instr-list) new-st))))