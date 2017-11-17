#lang s-exp rosette/safe

(require racket/list
         racket/base)

(provide add
         sub
         copyfrom
         copyto
         outbox
         (struct-out state))

(struct state (reg mem output) #:transparent)

(define (add loc st)
  (let* ([reg (state-reg st)]
         [mem (state-mem st)]
         [output (state-output st)]
         [x (vector-ref mem loc)])
    (cond
      [(null? reg) (reg-err)]
      [(null? x) (mem-err loc)]
      [else (state (+ reg x) mem output)])))

(define (sub loc st)
  (let* ([reg (state-reg st)]
         [mem (state-mem st)]
         [output (state-output st)]
         [x (vector-ref mem loc)])
    (cond
      [(null? reg) (reg-err)]
      [(null? x) (mem-err loc)]
      [else (state (- reg x) mem output)])))

(define (copyfrom loc st)
  (let* ([mem (state-mem st)]
         [output (state-output st)]
         [x (vector-ref mem loc)])
    (if (null? x)
        (mem-err loc)
        (state x mem output))))

(define (copyto loc st)
  (let* ([mem (state-mem st)]
         [output (state-output st)]
         [reg (state-reg st)]
         [newmem (list-set mem loc reg)])
    (if (null? reg)
        (reg-err)
        (state reg newmem output))))

(define (outbox st)
  (let* ([reg (state-reg st)]
         [mem (state-mem st)]
         [output (state-output st)]
         [newoutput (append output (list reg))])
    (if (null? reg)
        (reg-err)
        (state reg mem newoutput))))


; helper functions
(define (mem-err loc)
  (error (string-append "invalid mem read at loc " (number->string loc))))

(define (reg-err)
  (error "invalid operation on null register"))
    
