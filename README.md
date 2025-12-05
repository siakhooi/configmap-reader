# configmap-reader

microservice to read and return content of a configmap


## Deploy to clusters

```
kubectl apply -f ./configmap-reader
```

## Use

### Port forwarding

```
kubectl port-forward svc/configmap-reader 8080:80
```

## Test

```bash
curl http://localhost:8080/config
```

- edit the configmap `configmap-reader-data` and call again will return latest value

## Links

- https://hub.docker.com/r/siakhooi/configmap-reader
- https://pypi.org/project/configmap_reader/
- https://github.com/siakhooi/configmap-reader
- https://sonarcloud.io/project/overview?id=siakhooi_configmap-reader
- https://qlty.sh/gh/siakhooi/projects/configmap-reader

## Badges

![GitHub](https://img.shields.io/github/license/siakhooi/configmap-reader?logo=github)
![GitHub last commit](https://img.shields.io/github/last-commit/siakhooi/configmap-reader?logo=github)
![GitHub tag (latest by date)](https://img.shields.io/github/v/tag/siakhooi/configmap-reader?logo=github)
![GitHub issues](https://img.shields.io/github/issues/siakhooi/configmap-reader?logo=github)
![GitHub closed issues](https://img.shields.io/github/issues-closed/siakhooi/configmap-reader?logo=github)
![GitHub pull requests](https://img.shields.io/github/issues-pr-raw/siakhooi/configmap-reader?logo=github)
![GitHub closed pull requests](https://img.shields.io/github/issues-pr-closed-raw/siakhooi/configmap-reader?logo=github)
![GitHub top language](https://img.shields.io/github/languages/top/siakhooi/configmap-reader?logo=github)
![GitHub language count](https://img.shields.io/github/languages/count/siakhooi/configmap-reader?logo=github)
![Lines of code](https://img.shields.io/tokei/lines/github/siakhooi/configmap-reader?logo=github)
![GitHub repo size](https://img.shields.io/github/repo-size/siakhooi/configmap-reader?logo=github)
![GitHub code size in bytes](https://img.shields.io/github/languages/code-size/siakhooi/configmap-reader?logo=github)

![Workflow](https://img.shields.io/badge/Workflow-github-purple)
![workflow](https://github.com/siakhooi/configmap-reader/actions/workflows/build.yaml/badge.svg)
![workflow](https://github.com/siakhooi/configmap-reader/actions/workflows/workflow-deployments.yml/badge.svg)

![Release](https://img.shields.io/badge/Release-github-purple)
![GitHub release (latest by date)](https://img.shields.io/github/v/release/siakhooi/configmap-reader?label=GPR%20release&logo=github)
![GitHub all releases](https://img.shields.io/github/downloads/siakhooi/configmap-reader/total?color=33cb56&logo=github)
![GitHub Release Date](https://img.shields.io/github/release-date/siakhooi/configmap-reader?logo=github)

![Quality-Qlty](https://img.shields.io/badge/Quality-Qlty-purple)
[![Maintainability](https://qlty.sh/gh/siakhooi/projects/configmap-reader/maintainability.svg)](https://qlty.sh/gh/siakhooi/projects/configmap-reader)
[![Code Coverage](https://qlty.sh/gh/siakhooi/projects/configmap-reader/coverage.svg)](https://qlty.sh/gh/siakhooi/projects/configmap-reader)

![Quality-Sonar](https://img.shields.io/badge/Quality-SonarCloud-purple)
[![Code Smells](https://sonarcloud.io/api/project_badges/measure?project=siakhooi_configmap-reader&metric=code_smells)](https://sonarcloud.io/summary/new_code?id=siakhooi_configmap-reader)
[![Duplicated Lines (%)](https://sonarcloud.io/api/project_badges/measure?project=siakhooi_configmap-reader&metric=duplicated_lines_density)](https://sonarcloud.io/summary/new_code?id=siakhooi_configmap-reader)
[![Bugs](https://sonarcloud.io/api/project_badges/measure?project=siakhooi_configmap-reader&metric=bugs)](https://sonarcloud.io/summary/new_code?id=siakhooi_configmap-reader)
[![Vulnerabilities](https://sonarcloud.io/api/project_badges/measure?project=siakhooi_configmap-reader&metric=vulnerabilities)](https://sonarcloud.io/summary/new_code?id=siakhooi_configmap-reader)
[![Technical Debt](https://sonarcloud.io/api/project_badges/measure?project=siakhooi_configmap-reader&metric=sqale_index)](https://sonarcloud.io/summary/new_code?id=siakhooi_configmap-reader)
[![Maintainability Rating](https://sonarcloud.io/api/project_badges/measure?project=siakhooi_configmap-reader&metric=sqale_rating)](https://sonarcloud.io/summary/new_code?id=siakhooi_configmap-reader)
[![Security Rating](https://sonarcloud.io/api/project_badges/measure?project=siakhooi_configmap-reader&metric=security_rating)](https://sonarcloud.io/summary/new_code?id=siakhooi_configmap-reader)
[![Reliability Rating](https://sonarcloud.io/api/project_badges/measure?project=siakhooi_configmap-reader&metric=reliability_rating)](https://sonarcloud.io/summary/new_code?id=siakhooi_configmap-reader)
[![Quality Gate Status](https://sonarcloud.io/api/project_badges/measure?project=siakhooi_configmap-reader&metric=alert_status)](https://sonarcloud.io/summary/new_code?id=siakhooi_configmap-reader)
[![Lines of Code](https://sonarcloud.io/api/project_badges/measure?project=siakhooi_configmap-reader&metric=ncloc)](https://sonarcloud.io/summary/new_code?id=siakhooi_configmap-reader)
[![Coverage](https://sonarcloud.io/api/project_badges/measure?project=siakhooi_configmap-reader&metric=coverage)](https://sonarcloud.io/summary/new_code?id=siakhooi_configmap-reader)
![Sonar Violations (short format)](https://img.shields.io/sonar/violations/siakhooi_configmap-reader?server=https%3A%2F%2Fsonarcloud.io)
![Sonar Violations (short format)](https://img.shields.io/sonar/blocker_violations/siakhooi_configmap-reader?server=https%3A%2F%2Fsonarcloud.io)
![Sonar Violations (short format)](https://img.shields.io/sonar/critical_violations/siakhooi_configmap-reader?server=https%3A%2F%2Fsonarcloud.io)
![Sonar Violations (short format)](https://img.shields.io/sonar/major_violations/siakhooi_configmap-reader?server=https%3A%2F%2Fsonarcloud.io)
![Sonar Violations (short format)](https://img.shields.io/sonar/minor_violations/siakhooi_configmap-reader?server=https%3A%2F%2Fsonarcloud.io)
![Sonar Violations (short format)](https://img.shields.io/sonar/info_violations/siakhooi_configmap-reader?server=https%3A%2F%2Fsonarcloud.io)
![Sonar Violations (long format)](https://img.shields.io/sonar/violations/siakhooi_configmap-reader?format=long&server=http%3A%2F%2Fsonarcloud.io)

[![Generic badge](https://img.shields.io/badge/Funding-BuyMeACoffee-33cb56.svg)](https://www.buymeacoffee.com/siakhooi)
[![Generic badge](https://img.shields.io/badge/Funding-Ko%20Fi-33cb56.svg)](https://ko-fi.com/siakhooi)

![visitors](https://hit-tztugwlsja-uc.a.run.app/?outputtype=badge&counter=ghmd-configmap-reader)
