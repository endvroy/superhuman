#lang s-exp rosette/safe

(require "instructions.rkt"
         racket/base
         racket/list)

(define (enumerate st inst-set k)
  (cond
    [(= k 0) '(())]
    [else (for/fold ([tail '()])
                    ([inst inst-set])
            (append (enu-inst inst st inst-set k) tail))]))

(define (enu-inst inst st inst-set k)
  (cond
    [(equal? inst add) (enu-add st inst-set k)]
    [(equal? inst sub) (enu-sub st inst-set k)]
    [else (error "invalid instructions")]))

; enumerate possible operations for different instructions
(define (enu-add st inst-set k)
  (let* ([reg (state-reg st)]
         [mem (state-mem st)])
    (for/fold ([tail '()])
              ([i (vector-length mem)])
      (append (let* ([x (vector-ref mem i)])
                (cond
                  [(null? reg) '()]
                  [(null? x)   '()]
                  [else (cons-lst (list add i) (enumerate (add i st) inst-set (- k 1)))]))
              tail))))

(define (enu-sub st inst-set k)
  (let* ([reg (state-reg st)]
         [mem (state-mem st)])
    (for/fold ([tail '()])
              ([i (vector-length mem)])
      (append (let* ([x (vector-ref mem i)])
                (cond
                  [(null? reg) '()]
                  [(null? x)   '()]
                  [else (cons-lst (list sub i) (enumerate (sub i st) inst-set (- k 1)))]))
              tail))))

; helper funcs
(define (cons-lst-lst lst1 lst2)
  (if (null? lst1)
      '()
      (cons (cons (car lst1) lst2) (cons-lst-lst (cdr lst1) lst2))
  )
)

(define (cons-lst i insts)
  (if (null? insts)
      '()
      (cons (cons i (car insts)) (cons-lst i (cdr insts)))
  )
)

(define st (state 1 (vector 1 null 3) '()))
(define inst-set (list add sub))

(display (enumerate st inst-set 3))
