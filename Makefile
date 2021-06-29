.PHONY : run build push

run:
	docker-compose up

build:
	docker build -t local-build/fetch_rewards_assessment .
	@$(eval fetch_rewards_assessment=`docker images local-build/fetch_rewards_assessment  --format "{{.ID}}"`)
	docker tag $(fetch_rewards_assessment) jondkelley/fetch_rewards_assessment:latest

push:
	docker push jondkelley/fetch_rewards_assessment:latest