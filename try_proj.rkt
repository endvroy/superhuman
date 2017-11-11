#lang s-exp rosette/safe

(require racket/list)

(struct state (reg mem output) #:transparent)

(define (add loc st)
  (let* ([reg (state-reg st)]
         [mem (state-mem st)]
         [output (state-output st)]
         [x (list-ref mem loc)])
    (state (+ reg x) mem output)))

(define (sub loc st)
  (let* ([reg (state-reg st)]
         [mem (state-mem st)]
         [output (state-output st)]
         [x (list-ref mem loc)])
    (state (- reg x) mem output)))

(define (copyfrom loc st)
  (let* ([mem (state-mem st)]
         [output (state-output st)]
         [x (list-ref mem loc)])
    (state x mem output)))

(define (copyto loc st)
  (let* ([mem (state-mem st)]
         [output (state-output st)]
         [reg (state-reg st)]
         [newmem (list-set mem loc reg)])
    (state reg newmem output)))

(define (outbox st)
  (let* ([reg (state-reg st)]
         [mem (state-mem st)]
         [output (state-output st)]
         [newoutput (append output (list reg))])
    (state reg mem newoutput)))

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
(copyfrom 2 st) ; 42
(copyto 1 st)
(outbox (copyfrom 2 st))
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