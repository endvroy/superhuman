#lang s-exp rosette/safe

(require racket/list)

(struct state (reg mem output) #:transparent)

(define (add loc st)
  (let* ([reg (state-reg st)]
         [mem (state-mem st)]
         [output (state-output st)]
         [x (list-ref mem loc)])
    (state (+ x reg) mem output)))

(define (all-operands st)
  (let ([mem (state-mem st)])
    (range (length mem))))

(define (all-operands* st)
  (let ([mem (state-mem st)])
    (range (+ 1 (length mem)))))

; tests
(define mem '(0 1 42 3))
(define st (state 1337 mem '()))
(add 2 st) ; 1379
(all-operands st) ; 0-3
(all-operands* st) ; 0-4

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

; tests
(define instr (list add 2))
(exec instr st) ; 1379
(define instr-list (list
                      (list add 2)
                      (list add 3)))
(interpret instr-list st) ; 1382