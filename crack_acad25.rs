use std::fs;
use std::path::Path;
use winreg::enums::*;
use winreg::RegKey;

fn main() {
    // RegKey path
    let hkml = RegKey::predef(HKEY_LOCAL_MACHINE);
    let path = r"SOFTWARE\Autodesk\AutoCAD\R25.0\ACAD-8101\Install";

    // Open the RegKey
    match hkml.open_subkey(path) {
        Ok(subkey) => {
            // Read install path from key
            match subkey.get_value::<String, &str>("INSTALLDIR") {
                Ok(install_dir) => {
                    let current_path = std::env::current_exe().expect("Err");

                    let _ = fs::copy(&current_path.parent().unwrap().join("acad.exe"), Path::new(&install_dir).join("acad.exe"));
                    let _ = fs::copy(&current_path.parent().unwrap().join("acad.exe.bak"), Path::new(&install_dir).join("acad.exe.bak"));
                }
                Err(e) => {
                    eprintln!("Error al leer el valor INSTALLDIR: {}", e);
                }
            }
        }
        Err(e) => {
            eprintln!("Error al abrir la clave del registro: {}", e);
        }
    }
}