COMPOSE_DIR := .

all: up

up:
	@echo "Starting LinkedIn bot in background..."
	docker compose -f $(COMPOSE_DIR)/docker-compose.yml up --build

start:
	@echo "Starting LinkedIn bot services..."
	docker compose -f $(COMPOSE_DIR)/docker-compose.yml start

down:
	@echo "Stopping LinkedIn bot..."
	docker compose -f $(COMPOSE_DIR)/docker-compose.yml down

stop:
	@echo "Stopping LinkedIn bot services (keeping containers)..."
	docker compose -f $(COMPOSE_DIR)/docker-compose.yml stop

restart: down up
	@echo "LinkedIn bot restarted!"

build:
	@echo "Rebuilding LinkedIn bot images..."
	docker compose -f $(COMPOSE_DIR)/docker-compose.yml build

logs:
	@echo "Showing LinkedIn bot logs..."
	docker compose -f $(COMPOSE_DIR)/docker-compose.yml logs -f

ps:
	@echo "LinkedIn bot containers status:"
	docker compose -f $(COMPOSE_DIR)/docker-compose.yml ps

clean:
	@echo "Removing LinkedIn bot containers and volumes..."
	docker compose -f $(COMPOSE_DIR)/docker-compose.yml down --volumes --remove-orphans

fclean: clean
	@echo "Full cleanup of LinkedIn bot (containers, images, volumes)..."
	docker compose -f $(COMPOSE_DIR)/docker-compose.yml down --rmi all --volumes --remove-orphans

f:
	@echo "Aggressive Docker system cleanup..."
	docker builder prune -a --force
	docker system prune -a --volumes --force
	docker volume prune --all --force

re: fclean all

.PHONY: all up start down stop restart build logs ps clean fclean f re