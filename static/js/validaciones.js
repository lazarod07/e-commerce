function mostrarPassword(){
    var obj = document.getElementById("password");
    var ojito=document.getElementById("ojito");
    
    if (obj.type=="password"){
        obj.type = "text";
        ojito.classList.toggle("far fa-eye-slash");
                
    }else{
        obj.type = "password";
        ojito.classList.toggle("far fa-eye");
        
    }
    
}
