# ============================================================
#  Makefile - Dompetku
#  Perintah mudah untuk mengelola Docker tanpa hafal command
# ============================================================

.PHONY: help setup run stop restart reset logs test clean

help:
	@echo ""
	@echo "  Dompetku - Daftar Perintah"
	@echo "  =========================="
	@echo "  make setup    - Setup awal (salin .env, build Docker)"
	@echo "  make run      - Jalankan semua service"
	@echo "  make stop     - Matikan semua service"
	@echo "  make restart  - Restart semua service"
	@echo "  make reset    - Hapus database dan mulai dari awal"
	@echo "  make logs     - Lihat log backend secara live"
	@echo "  make test     - Jalankan semua unit test"
	@echo "  make clean    - Hapus semua container dan image Docker"
	@echo ""

setup:
	@echo ">> Menyalin .env.example ke .env ..."
	@cp -n .env.example .env || echo ".env sudah ada, dilewati."
	@echo ">> Build Docker image ..."
	docker compose build
	@echo ""
	@echo "Setup selesai! Sekarang jalankan: make run"

run:
	@echo ">> Menjalankan semua service ..."
	docker compose up -d
	@echo ""
	@echo "Aplikasi berjalan di:"
	@echo "  Backend    -> http://localhost:5000"
	@echo "  phpMyAdmin -> http://localhost:8080"

stop:
	@echo ">> Mematikan semua service ..."
	docker compose down

restart: stop run

reset:
	@echo ">> PERINGATAN: Semua data database akan dihapus!"
	@read -p "Lanjutkan? (y/N): " confirm && [ "$$confirm" = "y" ]
	docker compose down -v
	docker compose up -d
	@echo "Reset selesai!"

logs:
	docker compose logs -f backend

test:
	@echo ">> Menjalankan unit test ..."
	docker compose exec backend python -m pytest /app/../tests/ -v

clean:
	@echo ">> Menghapus semua container dan image Dompetku ..."
	docker compose down -v --rmi local
	@echo "Bersih!"
