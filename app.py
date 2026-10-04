import os
import sys
import re
import shutil
import subprocess
import urllib.request
import webbrowser
import json
from datetime import datetime


# ============================================================
# PIYXOX LARAVEL 12 + FILAMENT 5 CRUD MANAGER
# ============================================================

APP_TITLE = "PIYXOX LARAVEL 12 + FILAMENT 5 CRUD MANAGER"

BASE_DIR = os.path.dirname(
    os.path.abspath(__file__)
)

LOCAL_COMPOSER = os.path.join(
    BASE_DIR,
    "composer.phar"
)


# ============================================================
# BASIC HELPER
# ============================================================

def clear_screen():
    os.system(
        "cls" if os.name == "nt" else "clear"
    )


def pause():
    input(
        "\nTekan [Enter] untuk melanjutkan..."
    )


def command_exists(command):
    return shutil.which(command) is not None


def run_command(
    command,
    description="",
    cwd=None
):
    """
    Jalankan command.
    Return True jika berhasil.
    """

    if description:
        print(
            f"\n[INFO] {description}..."
        )

    print(
        f"[RUNNING] {command}"
    )

    try:

        result = subprocess.run(
            command,
            shell=True,
            cwd=cwd
        )

        if result.returncode != 0:

            print(
                "\n[ERROR] Command gagal."
            )

            print(
                f"[ERROR] Exit code: "
                f"{result.returncode}"
            )

            return False

        return True

    except Exception as e:

        print(
            f"\n[ERROR] Exception:"
            f"\n{e}"
        )

        return False


def run_command_capture(
    command,
    cwd=None
):
    """
    Jalankan command dan capture output.
    """

    try:

        result = subprocess.run(
            command,
            shell=True,
            cwd=cwd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )

        return (
            result.returncode,
            result.stdout,
            result.stderr
        )

    except Exception as e:

        return (
            1,
            "",
            str(e)
        )


# ============================================================
# PHP CHECK
# ============================================================

def get_php_version():

    try:

        result = subprocess.run(
            ["php", "-v"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )

        if result.returncode != 0:
            return None

        match = re.search(
            r"PHP\s+(\d+)\.(\d+)\.(\d+)",
            result.stdout
        )

        if not match:
            return None

        return tuple(
            map(
                int,
                match.groups()
            )
        )

    except Exception:

        return None


def check_php():

    print(
        "\n--- Memeriksa Versi PHP ---"
    )

    if not command_exists("php"):

        print(
            "[ERROR] PHP tidak ditemukan "
            "di PATH."
        )

        print(
            "Laravel 12 membutuhkan PHP 8.2+."
        )

        return False

    version = get_php_version()

    if version is None:

        print(
            "[ERROR] Tidak dapat membaca "
            "versi PHP."
        )

        return False

    major, minor, patch = version

    print(
        f"[INFO] PHP Version: "
        f"{major}.{minor}.{patch}"
    )

    if (major, minor) < (8, 2):

        print(
            "[ERROR] PHP harus 8.2 atau lebih baru."
        )

        return False

    print(
        "[SUKSES] PHP memenuhi syarat Laravel 12."
    )

    return True


# ============================================================
# COMPOSER
# ============================================================

def get_composer_command():

    if command_exists("composer"):
        return "composer"

    if os.path.exists(
        LOCAL_COMPOSER
    ):

        return (
            f'php "{LOCAL_COMPOSER}"'
        )

    return None


def composer_command():

    command = get_composer_command()

    if command:
        return command

    raise RuntimeError(
        "Composer tidak ditemukan."
    )


def install_local_composer():

    print(
        "\n[INFO] Composer global tidak ditemukan."
    )

    print(
        "[INFO] Mengunduh Composer..."
    )

    try:

        urllib.request.urlretrieve(
            "https://getcomposer.org/composer.phar",
            LOCAL_COMPOSER
        )

        if os.path.exists(
            LOCAL_COMPOSER
        ):

            print(
                "[SUKSES] composer.phar berhasil "
                "diunduh."
            )

            return True

    except Exception as e:

        print(
            f"[ERROR] Gagal mengunduh Composer:"
            f"\n{e}"
        )

    return False


def check_composer():

    print(
        "\n--- Memeriksa Composer ---"
    )

    composer = get_composer_command()

    if composer:

        code, stdout, stderr = (
            run_command_capture(
                f"{composer} --version"
            )
        )

        if code == 0:

            print(
                stdout.strip()
            )

            print(
                "[SUKSES] Composer siap digunakan."
            )

            return True

    if not install_local_composer():

        return False

    composer = get_composer_command()

    if not composer:
        return False

    code, stdout, stderr = (
        run_command_capture(
            f"{composer} --version"
        )
    )

    if code != 0:

        print(
            "[ERROR] Composer tidak dapat "
            "dijalankan."
        )

        return False

    print(
        stdout.strip()
    )

    print(
        "[SUKSES] Composer lokal siap."
    )

    return True


# ============================================================
# LARAVEL PROJECT CHECK
# ============================================================

def is_laravel_project(
    project_path
):

    return (
        os.path.isdir(project_path)
        and os.path.isfile(
            os.path.join(
                project_path,
                "artisan"
            )
        )
        and os.path.isfile(
            os.path.join(
                project_path,
                "composer.json"
            )
        )
        and os.path.isdir(
            os.path.join(
                project_path,
                "app"
            )
        )
    )


# ============================================================
# COMPOSER.JSON
# ============================================================

def read_composer_json():

    path = "composer.json"

    if not os.path.exists(path):
        return {}

    try:

        with open(
            path,
            "r",
            encoding="utf-8"
        ) as file:

            return json.load(
                file
            )

    except Exception:

        return {}


def get_filament_requirement():

    composer = read_composer_json()

    require = composer.get(
        "require",
        {}
    )

    return require.get(
        "filament/filament"
    )


def detect_filament_version():

    requirement = (
        get_filament_requirement()
    )

    if not requirement:
        return None

    requirement = str(
        requirement
    ).lower()

    # Filament 5
    if (
        "^5"
        in requirement
        or "5." in requirement
        or requirement == "5"
    ):

        return 5

    # Filament 4
    if (
        "^4"
        in requirement
        or "4." in requirement
        or requirement == "4"
    ):

        return 4

    # Filament 3
    if (
        "^3"
        in requirement
        or "3." in requirement
        or requirement == "3"
    ):

        return 3

    return None


# ============================================================
# DETECT OLD FILAMENT RESOURCE
# ============================================================

def find_filament_resource_files():

    resources = []

    root = os.path.join(
        "app",
        "Filament"
    )

    if not os.path.isdir(root):
        return resources

    for current_root, dirs, files in os.walk(
        root
    ):

        for filename in files:

            if not filename.endswith(
                ".php"
            ):
                continue

            full_path = os.path.join(
                current_root,
                filename
            )

            resources.append(
                full_path
            )

    return resources


def is_old_filament_resource(
    path
):
    """
    Mendeteksi pola API Filament lama.

    Tidak hanya berdasarkan versi composer,
    karena kasus kepet adalah:
        Filament 5 package
        tetapi Resource Filament 3.
    """

    try:

        with open(
            path,
            "r",
            encoding="utf-8"
        ) as file:

            content = file.read()

    except Exception:

        return False

    old_patterns = [

        # Filament 3 navigationIcon
        r"protected\s+static\s+\?string\s+\$navigationIcon",

        # Filament 3 form signature
        r"public\s+static\s+function\s+form\s*\(\s*Form\s+\$form\s*\)\s*:\s*Form",

        # Filament 3 table signature
        r"public\s+static\s+function\s+table\s*\(\s*Table\s+\$table\s*\)\s*:\s*Table",

        # Filament 3 old imports
        r"use\s+Filament\\Forms\\Form;",

        r"use\s+Filament\\Tables\\Table;",
    ]

    matches = 0

    for pattern in old_patterns:

        if re.search(
            pattern,
            content
        ):

            matches += 1

    # Jika minimal 2 pola lama ditemukan,
    # anggap resource lama.
    return matches >= 2


def find_old_filament_resources():

    old_resources = []

    for path in find_filament_resource_files():

        filename = os.path.basename(
            path
        )

        # Fokus pada Resource
        if not filename.endswith(
            "Resource.php"
        ):
            continue

        if is_old_filament_resource(
            path
        ):

            old_resources.append(
                path
            )

    return old_resources


# ============================================================
# BACKUP FILAMENT RESOURCE
# ============================================================

def backup_old_filament_resources():

    filament_path = os.path.join(
        "app",
        "Filament"
    )

    if not os.path.isdir(
        filament_path
    ):

        print(
            "[INFO] app/Filament belum ada."
        )

        return True

    old_resources = (
        find_old_filament_resources()
    )

    if not old_resources:

        print(
            "[INFO] Tidak ditemukan Resource "
            "Filament lama."
        )

        return True

    print(
        "\n[WARNING] Resource Filament lama "
        "terdeteksi!"
    )

    print(
        "[INFO] Resource yang terdeteksi:"
    )

    for resource in old_resources:

        print(
            f"       {resource}"
        )

    backup_name = (
        "Filament_Backup_"
        + datetime.now().strftime(
            "%Y%m%d_%H%M%S"
        )
    )

    backup_path = os.path.join(
        "app",
        backup_name
    )

    try:

        shutil.move(
            filament_path,
            backup_path
        )

        print(
            "\n[SUKSES] Folder Filament lama "
            "dibackup."
        )

        print(
            f"[INFO] Backup:"
        )

        print(
            f"       {backup_path}"
        )

        return True

    except Exception as e:

        print(
            "\n[ERROR] Gagal backup "
            "Filament lama:"
        )

        print(
            e
        )

        return False


# ============================================================
# CREATE LARAVEL PROJECT
# ============================================================

def create_laravel_project():

    print(
        "\n=========================================================="
    )

    print(
        "                 CREATE LARAVEL 12"
    )

    print(
        "=========================================================="
    )

    project_name = input(
        "Nama folder project "
        "(contoh: kepet): "
    ).strip()

    if not project_name:

        print(
            "[ERROR] Nama project kosong."
        )

        return None

    if not re.match(
        r"^[A-Za-z0-9._-]+$",
        project_name
    ):

        print(
            "[ERROR] Nama project tidak valid."
        )

        return None

    if os.path.exists(
        project_name
    ):

        existing_path = os.path.abspath(
            project_name
        )

        if is_laravel_project(
            existing_path
        ):

            answer = input(
                "Project Laravel sudah ada. "
                "Gunakan? (y/n): "
            ).strip().lower()

            if answer == "y":

                return project_name

        print(
            "[ERROR] Folder sudah ada."
        )

        return None

    composer = composer_command()

    command = (
        f'{composer} create-project '
        f'laravel/laravel '
        f'"{project_name}" '
        f'"^12.0" '
        f'--prefer-dist '
        f'--no-interaction'
    )

    if not run_command(
        command,
        "Membuat Laravel 12"
    ):

        return None

    print(
        "\n[SUKSES] Laravel 12 berhasil dibuat."
    )

    return project_name


# ============================================================
# ENV
# ============================================================

def update_env_value(
    content,
    key,
    value
):

    pattern = (
        rf"(?m)^\s*#?\s*"
        rf"{re.escape(key)}=.*$"
    )

    replacement = (
        f"{key}={value}"
    )

    if re.search(
        pattern,
        content
    ):

        return re.sub(
            pattern,
            replacement,
            content,
            count=1
        )

    if not content.endswith(
        "\n"
    ):

        content += "\n"

    return (
        content
        + replacement
        + "\n"
    )


def setup_env_file():

    if os.path.exists(
        ".env"
    ):

        return True

    if not os.path.exists(
        ".env.example"
    ):

        print(
            "[ERROR] .env.example tidak ditemukan."
        )

        return False

    shutil.copyfile(
        ".env.example",
        ".env"
    )

    print(
        "[SUKSES] .env dibuat."
    )

    return True


# ============================================================
# MYSQL
# ============================================================

def create_mysql_database(
    db_name,
    db_host,
    db_port,
    db_user,
    db_pass
):

    print(
        "\n--- Membuat Database MySQL ---"
    )

    def php_escape(
        value
    ):

        return (
            value
            .replace(
                "\\",
                "\\\\"
            )
            .replace(
                '"',
                '\\"'
            )
        )

    host = php_escape(
        db_host
    )

    port = php_escape(
        db_port
    )

    username = php_escape(
        db_user
    )

    password = php_escape(
        db_pass
    )

    database = php_escape(
        db_name
    )

    script = f'''<?php

$host = "{host}";
$port = "{port}";
$username = "{username}";
$password = "{password}";
$database = "{database}";

try {{

    $pdo = new PDO(
        "mysql:host={{$host}};port={{$port}}",
        $username,
        $password,
        [
            PDO::ATTR_ERRMODE =>
                PDO::ERRMODE_EXCEPTION
        ]
    );

    $safeDatabase = str_replace(
        "`",
        "``",
        $database
    );

    $sql =
        "CREATE DATABASE IF NOT EXISTS `"
        . $safeDatabase
        . "` CHARACTER SET utf8mb4 "
        . "COLLATE utf8mb4_unicode_ci";

    $pdo->exec($sql);

    echo "DATABASE_CREATED_SUCCESS";

}} catch (Throwable $e) {{

    echo "DATABASE_ERROR: "
        . $e->getMessage();

}}
?>'''

    temp_file = os.path.join(
        os.getcwd(),
        ".piyxox_create_database.php"
    )

    try:

        with open(
            temp_file,
            "w",
            encoding="utf-8"
        ) as file:

            file.write(
                script
            )

        code, stdout, stderr = (
            run_command_capture(
                f'php "{temp_file}"'
            )
        )

        output = stdout.strip()

        if (
            "DATABASE_CREATED_SUCCESS"
            in output
        ):

            print(
                f"[SUKSES] Database "
                f"'{db_name}' siap."
            )

            return True

        print(
            "[WARNING] Database gagal dibuat."
        )

        print(
            output
        )

        if stderr.strip():

            print(
                stderr.strip()
            )

        return False

    finally:

        if os.path.exists(
            temp_file
        ):

            try:

                os.remove(
                    temp_file
                )

            except Exception:
                pass


def setup_mysql_env():

    print(
        "\n--- Konfigurasi Database MySQL ---"
    )

    if not setup_env_file():

        return False

    db_name = input(
        "Nama Database "
        "(default: laravel_db): "
    ).strip()

    if not db_name:
        db_name = "laravel_db"

    db_host = input(
        "Database Host "
        "(default: 127.0.0.1): "
    ).strip()

    if not db_host:
        db_host = "127.0.0.1"

    db_port = input(
        "Database Port "
        "(default: 3306): "
    ).strip()

    if not db_port:
        db_port = "3306"

    db_user = input(
        "Database Username "
        "(default: root): "
    ).strip()

    if not db_user:
        db_user = "root"

    db_pass = input(
        "Database Password "
        "(kosong jika tidak ada): "
    ).strip()

    create_mysql_database(
        db_name,
        db_host,
        db_port,
        db_user,
        db_pass
    )

    with open(
        ".env",
        "r",
        encoding="utf-8"
    ) as file:

        content = file.read()

    values = {

        "DB_CONNECTION":
            "mysql",

        "DB_HOST":
            db_host,

        "DB_PORT":
            db_port,

        "DB_DATABASE":
            db_name,

        "DB_USERNAME":
            db_user,

        "DB_PASSWORD":
            db_pass,
    }

    for key, value in values.items():

        content = update_env_value(
            content,
            key,
            value
        )

    with open(
        ".env",
        "w",
        encoding="utf-8"
    ) as file:

        file.write(
            content
        )

    print(
        "[SUKSES] .env berhasil dikonfigurasi."
    )

    return True


# ============================================================
# FILAMENT INSTALL / UPGRADE
# ============================================================

def install_filament():

    print(
        "\n--- Memeriksa Filament ---"
    )

    version = (
        detect_filament_version()
    )

    print(
        f"[INFO] Filament composer requirement: "
        f"{version if version else 'tidak ada'}"
    )

    composer = composer_command()

    # --------------------------------------------------------
    # OLD VERSION
    # --------------------------------------------------------

    if version in (
        3,
        4
    ):

        print(
            f"[WARNING] Filament {version} "
            f"terdeteksi."
        )

        if not backup_old_filament_resources():

            return False

        command = (
            f'{composer} require '
            f'filament/filament:"^5.0" '
            f'--with-all-dependencies '
            f'--prefer-dist '
            f'--no-interaction'
        )

        if not run_command(
            command,
            "Upgrade ke Filament 5"
        ):

            return False

    # --------------------------------------------------------
    # FILAMENT 5
    # --------------------------------------------------------

    elif version == 5:

        print(
            "[INFO] Filament 5 terdeteksi."
        )

        # PENTING:
        # Composer bisa sudah Filament 5
        # tetapi Resource masih Filament 3.
        if not backup_old_filament_resources():

            return False

        print(
            "[INFO] Filament package sudah versi 5."
        )

    # --------------------------------------------------------
    # NONE
    # --------------------------------------------------------

    else:

        command = (
            f'{composer} require '
            f'filament/filament:"^5.0" '
            f'--with-all-dependencies '
            f'--prefer-dist '
            f'--no-interaction'
        )

        if not run_command(
            command,
            "Menginstall Filament 5"
        ):

            return False

    # --------------------------------------------------------
    # PANEL
    # --------------------------------------------------------

    if not run_command(
        "php artisan filament:install "
        "--panels "
        "--no-interaction",
        "Menyiapkan Filament Panel"
    ):

        return False

    print(
        "[SUKSES] Filament 5 berhasil disiapkan."
    )

    return True


# ============================================================
# LOGIN ROUTE
# ============================================================

def fix_login_route():
    """
    Filament menangani route login sendiri.

    Jangan membuat route /login yang mengarah langsung
    ke filament.admin.auth.login karena nama route
    tersebut tidak selalu tersedia pada versi Filament
    yang digunakan.
    """

    path = os.path.join(
        "routes",
        "web.php"
    )

    if not os.path.exists(path):

        print(
            "[WARNING] routes/web.php tidak ditemukan."
        )

        return False

    try:

        with open(
            path,
            "r",
            encoding="utf-8"
        ) as file:

            content = file.read()

    except Exception as e:

        print(
            "[ERROR] Gagal membaca routes/web.php:"
        )

        print(e)

        return False

    # ========================================================
    # HAPUS ROUTE LOGIN LAMA
    # ========================================================

    old_patterns = [

        # ----------------------------------------------------
        # Pattern standar generator lama
        # ----------------------------------------------------

        r"Route::get\('/login',\s*function\s*\(\)\s*\{\s*"
        r"return\s+redirect\(\)->route\(\s*"
        r"['\"]filament\.admin\.auth\.login['\"]\s*"
        r"\);\s*"
        r"\}\)->name\('login'\);\s*",

        # ----------------------------------------------------
        # Pattern dengan name login menggunakan double quote
        # ----------------------------------------------------

        r'Route::get\("/login",\s*function\s*\(\)\s*\{\s*'
        r"return\s+redirect\(\)->route\(\s*"
        r"['\"]filament\.admin\.auth\.login['\"]\s*"
        r"\);\s*"
        r'\}\)->name\(["\']login["\']\);\s*',
    ]

    original_content = content

    for pattern in old_patterns:

        content = re.sub(
            pattern,
            "",
            content,
            flags=re.MULTILINE
        )

    # ========================================================
    # JIKA TIDAK ADA PERUBAHAN
    # ========================================================

    if content == original_content:

        print(
            "[INFO] Route /login lama tidak ditemukan."
        )

    else:

        print(
            "[SUKSES] Route /login lama dihapus."
        )

    # ========================================================
    # TULIS KEMBALI WEB.PHP
    # ========================================================

    try:

        with open(
            path,
            "w",
            encoding="utf-8"
        ) as file:

            file.write(
                content
            )

        print(
            "[SUKSES] routes/web.php diperbaiki."
        )

    except Exception as e:

        print(
            "[ERROR] Gagal menulis routes/web.php:"
        )

        print(e)

        return False

    return True


# ============================================================
# SETUP ENVIRONMENT
# ============================================================
def setup_environment():
    print(
        "\n=========================================================="
    )
    print(
        "                 SETUP ENVIRONMENT"
    )
    print(
        "=========================================================="
    )

    # ========================================================
    # STEP 1
    # BACKUP RESOURCE FILAMENT SEBELUM ARTISAN APAPUN
    # ========================================================

    print(
        "\n--- Memeriksa Resource Filament Lama ---"
    )

    if not backup_old_filament_resources():
        print(
            "[ERROR] Tidak dapat mengamankan "
            "Resource Filament lama."
        )
        return False

    # ========================================================
    # STEP 2
    # DATABASE
    # ========================================================

    if not setup_mysql_env():
        print(
            "[ERROR] Setup MySQL gagal."
        )
        return False

    # ========================================================
    # STEP 3
    # APP KEY
    # ========================================================

    if not run_command(
        "php artisan key:generate",
        "Generate Application Key"
    ):
        print(
            "[ERROR] key:generate gagal."
        )
        return False

    # ========================================================
    # STEP 4
    # FILAMENT
    # ========================================================

    if not install_filament():
        print(
            "[ERROR] Instalasi Filament gagal."
        )
        return False

    # ========================================================
    # STEP 5
    # LOGIN ROUTE
    # ========================================================

    fix_login_route()

    # ========================================================
    # STEP 6
    # SESSION
    # ========================================================

    print(
        "\n--- Menyiapkan Session Laravel ---"
    )

    session_migration_dir = os.path.join(
        "database",
        "migrations"
    )

    session_migration_exists = False

    # --------------------------------------------------------
    # Cari migration sessions dengan lebih fleksibel
    # --------------------------------------------------------

    if os.path.isdir(session_migration_dir):

        for filename in os.listdir(
            session_migration_dir
        ):

            filename_lower = filename.lower()

            if not filename_lower.endswith(".php"):
                continue

            # Laravel bisa menggunakan nama:
            #
            # xxxx_xx_xx_xxxxxx_create_sessions_table.php
            #
            # atau migration lain yang mengandung sessions.

            if (
                "create_sessions_table"
                in filename_lower
                or
                "sessions_table"
                in filename_lower
            ):
                session_migration_exists = True
                break

    # ========================================================
    # JIKA MIGRATION SUDAH ADA
    # ========================================================

    if session_migration_exists:

        print(
            "[INFO] Migration sessions sudah tersedia."
        )

    # ========================================================
    # JIKA MIGRATION BELUM TERDETEKSI
    # ========================================================

    else:

        print(
            "[INFO] Migration sessions belum terdeteksi."
        )

        print(
            "[INFO] Memeriksa dengan artisan..."
        )

        # ----------------------------------------------------
        # Jalankan session:table tetapi CAPTURE output.
        # Jangan langsung anggap gagal.
        # ----------------------------------------------------

        code, stdout, stderr = (
            run_command_capture(
                "php artisan session:table"
            )
        )

        output = (
            (stdout or "")
            + "\n"
            + (stderr or "")
        ).strip()

        # ----------------------------------------------------
        # SUCCESS
        # ----------------------------------------------------

        if code == 0:

            print(
                "[SUKSES] Migration sessions berhasil dibuat."
            )

            session_migration_exists = True

        # ----------------------------------------------------
        # SUDAH ADA
        # ----------------------------------------------------

        elif (
            "Migration already exists"
            in output
            or
            "already exists"
            in output
        ):

            print(
                "[INFO] Migration sessions sudah ada."
            )

            print(
                "[INFO] Melanjutkan proses."
            )

            session_migration_exists = True

        # ----------------------------------------------------
        # ERROR LAIN
        # ----------------------------------------------------

        else:

            print(
                "[ERROR] Gagal menyiapkan migration sessions."
            )

            print(
                "\nDetail:"
            )

            if stdout.strip():
                print(stdout.strip())

            if stderr.strip():
                print(stderr.strip())

            return False

    # ========================================================
    # STEP 7
    # DATABASE MIGRATION
    # ========================================================

    print(
        "\n--- Database Migration ---"
    )

    print(
        "[INFO] Menjalankan php artisan migrate."
    )

    print(
        "[INFO] migrate:fresh TIDAK digunakan."
    )

    print(
        "[INFO] Database/data existing tidak akan "
        "dihapus."
    )

    if not run_command(
        "php artisan migrate",
        "Menjalankan Migration"
    ):

        print(
            "\n[ERROR] Database migration gagal."
        )

        print(
            "[INFO] Tidak menjalankan migrate:fresh."
        )

        return False

    # ========================================================
    # STEP 8
    # CLEAR CACHE
    # ========================================================

    print(
        "\n--- Membersihkan Cache ---"
    )

    if not run_command(
        "php artisan optimize:clear",
        "Membersihkan Laravel Cache"
    ):

        print(
            "[WARNING] optimize:clear gagal."
        )

    # ========================================================
    # STEP 9
    # CEK STATUS MIGRATION
    # ========================================================

    print(
        "\n--- Mengecek Status Migration ---"
    )

    code, stdout, stderr = (
        run_command_capture(
            "php artisan migrate:status"
        )
    )

    if code == 0:

        print(
            stdout.strip()
        )

    else:

        print(
            "[WARNING] Tidak dapat membaca "
            "status migration."
        )

        if stderr.strip():
            print(
                stderr.strip()
            )

    # ========================================================
    # STEP 10
    # VERIFY SESSION TABLE
    # ========================================================

    print(
        "\n--- Verifikasi Session Table ---"
    )

    # Gunakan artisan tinker untuk memastikan
    # tabel sessions benar-benar tersedia.

    verify_command = (
        'php artisan tinker --execute='
        '"Schema::hasTable(\'sessions\') ? '
        'print(\'SESSION_TABLE_OK\') : '
        'print(\'SESSION_TABLE_MISSING\');"'
    )

    code, stdout, stderr = (
        run_command_capture(
            verify_command
        )
    )

    verification_output = (
        (stdout or "")
        + "\n"
        + (stderr or "")
    )

    if "SESSION_TABLE_OK" in verification_output:

        print(
            "[SUKSES] Tabel sessions tersedia."
        )

    else:

        print(
            "[WARNING] Tabel sessions belum terdeteksi."
        )

        print(
            "[INFO] Periksa migration dan database."
        )

    # ========================================================
    # SUCCESS
    # ========================================================

    print(
        "\n=========================================================="
    )

    print(
        "[SUKSES] Setup Environment selesai."
    )

    print(
        "=========================================================="
    )

    print(
        "\nDatabase : fufu"
    )

    print(
        "Laravel  : Laravel 12"
    )

    print(
        "Filament : Filament 5"
    )

    print(
        "Session  : Database"
    )

    print(
        "\nAdmin URL:"
    )

    print(
        "http://127.0.0.1:8000/admin"
    )

    print(
        "=========================================================="
    )

    return True


# ============================================================
# MODEL UTILITIES
# ============================================================

def normalize_model_name(
    name
):

    parts = re.split(
        r"[_\-\s]+",
        name
    )

    return "".join(
        part[:1].upper()
        + part[1:]
        for part in parts
        if part
    )


def model_to_table(
    model_name
):

    snake = re.sub(
        r"(?<!^)(?=[A-Z])",
        "_",
        model_name
    ).lower()

    if snake.endswith("y"):

        return (
            snake[:-1]
            + "ies"
        )

    if snake.endswith("s"):

        return (
            snake
            + "es"
        )

    return (
        snake
        + "s"
    )


# ============================================================
# ASK COLUMNS
# ============================================================

def ask_columns():

    columns = []

    relations = []

    print(
        "\n=========================================================="
    )

    print(
        "                    DEFINE COLUMNS"
    )

    print(
        "=========================================================="
    )

    while True:

        name = input(
            "\nNama Kolom "
            "(ketik 'selesai'): "
        ).strip()

        if name.lower() == "selesai":

            if not columns:

                print(
                    "[WARNING] Minimal 1 kolom."
                )

                continue

            break

        if not name:

            print(
                "[WARNING] Nama kolom kosong."
            )

            continue

        if not re.match(
            r"^[A-Za-z_][A-Za-z0-9_]*$",
            name
        ):

            print(
                "[ERROR] Nama kolom tidak valid."
            )

            continue

        print(
            "\n1. string"
        )

        print(
            "2. text"
        )

        print(
            "3. integer"
        )

        print(
            "4. bigInteger"
        )

        print(
            "5. boolean"
        )

        print(
            "6. decimal"
        )

        print(
            "7. date"
        )

        print(
            "8. dateTime"
        )

        print(
            "9. foreignId"
        )

        choice = input(
            "Pilih tipe (1-9): "
        ).strip()

        type_map = {

            "1":
                "string",

            "2":
                "text",

            "3":
                "integer",

            "4":
                "bigInteger",

            "5":
                "boolean",

            "6":
                "decimal",

            "7":
                "date",

            "8":
                "dateTime",

            "9":
                "foreignId",
        }

        col_type = type_map.get(
            choice,
            "string"
        )

        extra = ""

        if col_type == "string":

            length = input(
                "Panjang VARCHAR "
                "(default 255): "
            ).strip()

            if not length:
                length = "255"

            if not length.isdigit():
                length = "255"

            extra = (
                f"->length({length})"
            )

        elif col_type == "decimal":

            precision = input(
                "Precision "
                "(default 15): "
            ).strip()

            scale = input(
                "Scale "
                "(default 2): "
            ).strip()

            if not precision:
                precision = "15"

            if not scale:
                scale = "2"

            if not precision.isdigit():
                precision = "15"

            if not scale.isdigit():
                scale = "2"

            extra = (
                f"->decimal("
                f"'{name}', "
                f"{precision}, "
                f"{scale}"
                f")"
            )

        elif col_type == "foreignId":

            related_name = (
                name.removesuffix(
                    "_id"
                )
            )

            related_model = (
                normalize_model_name(
                    related_name
                )
            )

            relations.append(
                {
                    "column":
                        name,

                    "model":
                        related_model
                }
            )

        columns.append(
            {
                "name":
                    name,

                "type":
                    col_type,

                "extra":
                    extra
            }
        )

        print(
            f"[OK] {name} "
            f"({col_type}) ditambahkan."
        )

    return (
        columns,
        relations
    )


# ============================================================
# GENERATE MIGRATION
# ============================================================

def generate_migration(
    table_name,
    columns
):

    migration_dir = os.path.join(
        "database",
        "migrations"
    )

    os.makedirs(
        migration_dir,
        exist_ok=True
    )

    timestamp = datetime.now().strftime(
        "%Y_%m_%d_%H%M%S"
    )

    filename = (
        f"{timestamp}"
        f"_create_{table_name}_table.php"
    )

    path = os.path.join(
        migration_dir,
        filename
    )

    lines = []

    for col in columns:

        name = col["name"]

        col_type = col["type"]

        extra = col["extra"]

        if col_type == "foreignId":

            related = (
                name.removesuffix(
                    "_id"
                )
            )

            related_model = (
                normalize_model_name(
                    related
                )
            )

            related_table = (
                model_to_table(
                    related_model
                )
            )

            lines.append(
                "            "
                f"$table->foreignId("
                f"'{name}'"
                f")->constrained("
                f"'{related_table}'"
                f")->cascadeOnDelete();"
            )

        elif col_type == "decimal":

            lines.append(
                "            "
                f"$table->{extra[2:]};"
            )

        else:

            lines.append(
                "            "
                f"$table->{col_type}("
                f"'{name}'"
                f")"
                f"{extra};"
            )

    schema = "\n".join(
        lines
    )

    content = f"""<?php

use Illuminate\\Database\\Migrations\\Migration;
use Illuminate\\Database\\Schema\\Blueprint;
use Illuminate\\Support\\Facades\\Schema;

return new class extends Migration
{{
    public function up(): void
    {{
        Schema::create('{table_name}', function (Blueprint $table) {{
            $table->id();
{schema}
            $table->timestamps();
        }});
    }}

    public function down(): void
    {{
        Schema::dropIfExists('{table_name}');
    }}
}};
"""

    with open(
        path,
        "w",
        encoding="utf-8"
    ) as file:

        file.write(
            content
        )

    print(
        f"[SUKSES] Migration dibuat:"
    )

    print(
        path
    )

    return path


# ============================================================
# UPDATE MODEL
# ============================================================

def update_model(
    model_name,
    columns,
    relations
):

    path = os.path.join(
        "app",
        "Models",
        f"{model_name}.php"
    )

    if not os.path.exists(path):

        print(
            "[WARNING] Model tidak ditemukan."
        )

        return False

    with open(
        path,
        "r",
        encoding="utf-8"
    ) as file:

        content = file.read()

    # --------------------------------------------------------
    # IMPORT
    # --------------------------------------------------------

    imports = []

    for relation in relations:

        related_model = (
            relation["model"]
        )

        if related_model == model_name:
            continue

        line = (
            f"use App\\Models\\"
            f"{related_model};"
        )

        if line not in content:

            imports.append(
                line
            )

    if imports:

        import_text = (
            "\n"
            + "\n".join(
                imports
            )
            + "\n"
        )

        marker = (
            "use Illuminate\\"
        )

        if marker in content:

            content = content.replace(
                marker,
                import_text
                + marker,
                1
            )

    # --------------------------------------------------------
    # FILLABLE
    # --------------------------------------------------------

    fields = ",\n        ".join(
        f"'{column['name']}'"
        for column in columns
    )

    content = re.sub(
        r"\s*protected\s+\$fillable"
        r"\s*=\s*\[.*?\];",
        "",
        content,
        flags=re.DOTALL
    )

    fillable = (
        "\n\n"
        "    protected $fillable = [\n"
        f"        {fields}\n"
        "    ];\n"
    )

    if "use HasFactory;" in content:

        content = content.replace(
            "use HasFactory;",
            "use HasFactory;"
            + fillable,
            1
        )

    # --------------------------------------------------------
    # RELATION
    # --------------------------------------------------------

    relation_code = ""

    for relation in relations:

        method = (
            relation["column"]
            .removesuffix(
                "_id"
            )
        )

        related_model = (
            relation["model"]
        )

        relation_code += f"""

    public function {method}()
    {{
        return $this->belongsTo(
            {related_model}::class,
            '{relation["column"]}'
        );
    }}
"""

    if relation_code:

        position = content.rfind(
            "}"
        )

        if position != -1:

            content = (
                content[:position]
                + relation_code
                + "\n"
                + content[position:]
            )

    with open(
        path,
        "w",
        encoding="utf-8"
    ) as file:

        file.write(
            content
        )

    print(
        "[SUKSES] Model berhasil diperbarui."
    )

    return True


# ============================================================
# DATABASE MODE
# ============================================================

def choose_database_mode():

    print(
        "\n=========================================================="
    )

    print(
        "                    DATABASE MODE"
    )

    print(
        "=========================================================="
    )

    print(
        "1. Buat tabel baru"
    )

    print(
        "2. Gunakan tabel existing"
    )

    choice = input(
        "\nPilih (1-2): "
    ).strip()

    if choice == "2":

        table = input(
            "Nama tabel existing: "
        ).strip()

        if not table:

            print(
                "[ERROR] Nama tabel kosong."
            )

            return None

        return {
            "mode":
                "existing",

            "table":
                table
        }

    return {
        "mode":
            "migration",

        "table":
            None
    }


# ============================================================
# CRUD
# ============================================================

def generate_crud_internal():

    print(
        "\n=========================================================="
    )

    print(
        "                  PIYXOX CRUD GENERATOR"
    )

    print(
        "=========================================================="
    )

    raw_name = input(
        "Nama Model "
        "(contoh: Produk): "
    ).strip()

    if not raw_name:

        print(
            "[ERROR] Nama model kosong."
        )

        return

    model_name = normalize_model_name(
        raw_name
    )

    database_mode = (
        choose_database_mode()
    )

    if database_mode is None:
        return

    if (
        database_mode["mode"]
        == "existing"
    ):

        table_name = (
            database_mode["table"]
        )

    else:

        table_name = (
            model_to_table(
                model_name
            )
        )

    columns, relations = (
        ask_columns()
    )

    # --------------------------------------------------------
    # MODEL
    # --------------------------------------------------------

    if not run_command(
        f"php artisan make:model "
        f"{model_name} "
        f"-f "
        f"--force",
        "Membuat Model & Factory"
    ):

        return

    # --------------------------------------------------------
    # SEEDER
    # --------------------------------------------------------

    answer = input(
        "\nBuat Seeder? (Y/n): "
    ).strip().lower()

    if answer != "n":

        run_command(
            f"php artisan make:seeder "
            f"{model_name}Seeder",
            "Membuat Seeder"
        )

    # --------------------------------------------------------
    # UPDATE MODEL
    # --------------------------------------------------------

    update_model(
        model_name,
        columns,
        relations
    )

    # --------------------------------------------------------
    # MIGRATION
    # --------------------------------------------------------

    if (
        database_mode["mode"]
        == "migration"
    ):

        migration_dir = os.path.join(
            "database",
            "migrations"
        )
        already_migrated = False
        if os.path.exists(migration_dir):
            for f in os.listdir(migration_dir):
                if f.endswith(f"_create_{table_name}_table.php"):
                    already_migrated = True
                    break

        if already_migrated:
            print(
                f"\n[INFO] Tabel {table_name} sudah ada migration-nya."
            )
            print(
                "[INFO] Mengubah otomatis ke mode Existing Table (Migration dilewati)."
            )
        else:
            generate_migration(
                table_name,
                columns
            )
    
            if not run_command(
                "php artisan migrate",
                "Menjalankan Migration"
            ):
    
                print(
                    "[WARNING] Migration gagal."
                )
    
                print(
                    "[INFO] migrate:fresh TIDAK dijalankan."
                )

    else:

        print(
            "\n[INFO] Existing Table Mode."
        )

        print(
            f"[INFO] Table: {table_name}"
        )

        print(
            "[INFO] Migration tidak dibuat."
        )

    # --------------------------------------------------------
    # FILAMENT RESOURCE
    # --------------------------------------------------------

    print(
        "\n--- Membuat Filament Resource ---"
    )

    command = (
        f"php artisan "
        f"make:filament-resource "
        f"{model_name} "
        f"--generate "
        f"--force"
    )

    if not run_command(
        command,
        "Generate Filament CRUD"
    ):

        print(
            "[ERROR] Filament Resource gagal."
        )

        return

    # --------------------------------------------------------
    # CACHE
    # --------------------------------------------------------

    run_command(
        "php artisan optimize:clear",
        "Membersihkan Cache"
    )

    print(
        "\n=========================================================="
    )

    print(
        "[SUKSES] CRUD berhasil dibuat."
    )

    print(
        "=========================================================="
    )

    print(
        f"Model   : app/Models/{model_name}.php"
    )

    print(
        f"Table   : {table_name}"
    )

    print(
        "Admin   : http://127.0.0.1:8000/admin"
    )


# ============================================================
# ADMIN
# ============================================================

def create_filament_user():

    print(
        "\n=========================================================="
    )

    print(
        "                 CREATE ADMIN"
    )

    print(
        "=========================================================="
    )

    run_command(
        "php artisan optimize:clear",
        "Membersihkan Cache sebelum membuat Admin"
    )

    run_command(
        "php artisan make:filament-user",
        "Membuat Admin Filament"
    )


# ============================================================
# SERVER
# ============================================================

def run_server():

    import socket
    port = 8000
    while True:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            if s.connect_ex(('127.0.0.1', port)) != 0:
                break
        port += 1

    url = (
        f"http://127.0.0.1:{port}/admin"
    )

    print(
        f"\n[INFO] Admin URL: {url}"
    )

    try:

        webbrowser.open(
            url
        )

        subprocess.run(
            f"php artisan serve --port={port}",
            shell=True
        )

    except KeyboardInterrupt:

        print(
            "\n[INFO] Server dihentikan."
        )


# ============================================================
# CLEAR CACHE
# ============================================================

def clear_laravel_cache():

    run_command(
        "php artisan optimize:clear",
        "Membersihkan Laravel Cache"
    )

    run_command(
        "composer dump-autoload",
        "Regenerate Composer Autoload"
    )


# ============================================================
# DASHBOARD
# ============================================================

def piyxox_dashboard(
    project_path
):

    original_dir = (
        os.getcwd()
    )

    try:

        os.chdir(
            project_path
        )

        while True:

            clear_screen()

            print(
                "=========================================================="
            )

            print(
                "     PIYXOX LARAVEL 12 + FILAMENT 5 CRUD MANAGER"
            )

            print(
                "=========================================================="
            )

            print(
                f"Project: "
                f"{os.path.basename(os.getcwd())}"
            )

            print()

            print(
                "1. Setup Environment "
                "(MySQL + Filament)"
            )

            print(
                "2. Buat Akun Admin Filament"
            )

            print(
                "3. Generate CRUD"
            )

            print(
                "4. Jalankan Server & Buka Admin"
            )

            print(
                "5. Clear Cache"
            )

            print(
                "6. Kembali ke Menu Utama"
            )

            choice = input(
                "\nPilih menu (1-6): "
            ).strip()

            if choice == "1":

                setup_environment()

                pause()

            elif choice == "2":

                create_filament_user()

                pause()

            elif choice == "3":

                generate_crud_internal()

                pause()

            elif choice == "4":

                run_server()

            elif choice == "5":

                clear_laravel_cache()

                pause()

            elif choice == "6":

                break

            else:

                print(
                    "[ERROR] Pilihan tidak valid."
                )

                pause()

    finally:

        os.chdir(
            original_dir
        )


# ============================================================
# EXISTING PROJECT
# ============================================================

def open_existing_project():

    path = input(
        "\nMasukkan path project Laravel: "
    ).strip().strip('"')

    if not path:

        print(
            "[ERROR] Path kosong."
        )

        return

    path = os.path.abspath(
        path
    )

    if not is_laravel_project(
        path
    ):

        print(
            "[ERROR] Folder bukan project "
            "Laravel yang valid."
        )

        return

    piyxox_dashboard(
        path
    )


# ============================================================
# MAIN
# ============================================================

def main():

    os.chdir(BASE_DIR)
    clear_screen()

    print(
        "=========================================================="
    )

    print(
        "       PIYXOX LARAVEL 12 + FILAMENT 5 GENERATOR"
    )

    print(
        "=========================================================="
    )

    print(
        "\nFitur:"
    )

    print(
        "• Laravel 12"
    )

    print(
        "• PHP 8.2+"
    )

    print(
        "• MySQL"
    )

    print(
        "• Filament 5"
    )

    print(
        "• Auto backup Resource Filament lama"
    )

    print(
        "• Model + Factory"
    )

    print(
        "• Seeder"
    )

    print(
        "• Migration"
    )

    print(
        "• Existing Database Table"
    )

    print(
        "• Filament CRUD"
    )

    print(
        "• Tidak menggunakan migrate:fresh"
    )

    if not check_php():

        input(
            "\nTekan Enter untuk keluar..."
        )

        sys.exit(1)

    if not check_composer():

        input(
            "\nTekan Enter untuk keluar..."
        )

        sys.exit(1)

    while True:

        clear_screen()

        print(
            "=========================================================="
        )

        print(
            "                    MENU UTAMA"
        )

        print(
            "=========================================================="
        )

        print(
            "1. Buat Project Laravel 12 Baru"
        )

        print(
            "2. Buka Project Laravel Existing"
        )

        print(
            "3. Keluar"
        )

        choice = input(
            "\nPilih menu (1-3): "
        ).strip()

        if choice == "1":

            project = (
                create_laravel_project()
            )

            if project:

                piyxox_dashboard(
                    project
                )

        elif choice == "2":

            open_existing_project()

            pause()

        elif choice == "3":

            print(
                "\nTerima kasih telah menggunakan "
                "PiyXoX Generator."
            )

            break

        else:

            print(
                "[ERROR] Pilihan tidak valid."
            )

            pause()


# ============================================================
# ENTRY POINT
# ============================================================

if __name__ == "__main__":

    main()