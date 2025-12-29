type student = {
  name : string;
  classe : string; (* Classe PCSI; MP2I; MPSI... *)
  age : int;
}

let rbg : student = { (** Le ': student' est facultatif *)
  name = "Matisse";
  classe = "MPI";
  age = 18;
}

