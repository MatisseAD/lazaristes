(** Quel est le type et la valeur des opérations suivantes : *)

let _ = print_endline @@ string_of_int @@ 7 * (1 +2 + 3)

(** Nous avons comme type un 'int' et en valeur '42'*)

let _ = print_endline @@ "CS " ^ string_of_int 3110

(** Nous avons comme type 'String' et en valeur 'CS 3110'*)

(** Write an expression that multiplies 42 by 10. *)

let _ = print_endline @@ string_of_int @@ 42*10 

(** Write an expression that divides 3.14 by 2.0. Hint: integer and floating-point operators are written differently in OCaml.*)

let _ = print_endline @@ string_of_float @@ 2.0 /. 3.14

(** Write an expression that computes 4.2 raised to the seventh power. Note: there is no built-in integer exponentiation operator in OCaml (nor is there in C, by the way), in part because it is not an operation provided by most CPUs.*)

let _ = print_endline @@ string_of_float @@ 4.2 ** 7.

(** Exercise: equality [★]

Write an expression that compares 42 to 42 using structural equality.

Write an expression that compares "hi" to "hi" using structural equality. What is the result?

Write an expression that compares "hi" to "hi" using physical equality. What is the result? *)

let _ = print_endline @@ "42 = 42"

let _ = print_endline @@ "'hi' = 'hi'" (** Les ' représentes les guillemets dans ce contexte*)
(** Cette dernière expression retourne vrai*)

let _ =  print_endline @@ "'hi' == 'hi'" (** //*)

(** Cette dernière expression retourne False*)

(**
Exercise: assert [★]

Enter assert true;; into utop and see what happens.

Enter assert false;; into utop and see what happens.

Write an expression that asserts 2110 is not (structurally) equal to 3110.
*)

let _ = assert (not(2110 = 3110))

let _ = if 2 > 1 then 42 else 7

let double x = x*2

let cube x = x *. x *. x

let sign_calculator x = if x < 0 then -1 else if x > 0 then 1 else 0

let circle_area rad = rad *. ( Float.pi *. Float.pi)

let rms x y = (x*.x +. y*.y) /. 2. |> sqrt

let date_fun d m = 
  if m = "Jan" || m = "Mar" || m = "May" || m = "Jul" || m = "Aug" || m = "Oct" || m = "Dec"
    then 
      if 0 < d && d < 32 then true else false
    else if m = "Feb" || m = "Apr" || m = "Jun" || m = "Sep" || m =  "Nov"
      then if 0 < d && d < 31 then true else false
else false

(** Fibo function *)

let rec fibo n = if n = 1 || n = 2 then 1 else fibo(n-1) + fibo(n-2)

(** Assertions parts *)

let _ = assert (double 4 = 8) (** Passed *)
let _ = assert (double 8 = 17) (** Raise an exception *)


