#lang s-exp rosette/safe

(require racket/list)

(struct state (reg mem output) #:transparent)

; exec one instr
(define (exec instr st)
  (let ([opcode (first instr)]
        [operands (append (rest instr) (list st))])
    (apply opcode operands)))

; interpret seq of instr
(define (interpret instr-list ip st)
  (if (empty? instr-list)
      st
      (let* ([instr (list-ref instr-list ip)]
             [opcode (first instr)])
        (cond
          [(= opcode 'jump) (let ([target (second instr)])
                              (interpret instr-list target st))]
          [(= opcode 'jump-if-zero) (let ([target (second instr)])
                                      (if (= 0 (state-reg st))
                                          (interpret instr-list target st)
                                          (interpret instr-list (+ 1 ip) st)))]
          [(= opcode 'jump-if-neg) (let ([target (second instr)])
                                     (if (< 0 (state-reg st))
                                         (interpret instr-list target st)
                                         (interpret instr-list (+ 1 ip) st)))]
          [else (define new-st (exec instr st))
                (interpret instr-list (+ 1 ip) new-st)]))))