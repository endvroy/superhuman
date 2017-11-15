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
    