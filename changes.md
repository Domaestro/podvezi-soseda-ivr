**[ Заявка ]**

Немного изменён образ продукта, что никак не сказывается на пользовательских сценариях. Конкретно: на базе веб-приложения не будет создана pwa-версия, в связи с ее нестабильной работой и нехватки времени на решение этих проблем. Вместо этого уже проделана колоссальная работа по замещению почтового сервера корпорации Google (которая с мая отказала в обслуживании), на свой собственный, работающий на домашнем сервере. Это заняло много времени и сил, в частности, пришлось много общаться с провайдером, чтобы письма, отправленные с сервера, проходили спам-фильтры российских (и не только) почтовых сервисов (Yandex, Mail.ru, Rambler). Также принято решение размещать свой сервис на том же домашнем сервере, из-за чего в средства разработки был добавлен Docker. Это тоже вносит свои трудности в проект, поскольку раньше мне не приходилось заниматься упаковкой проектов в контейнеры.

**[ Пользовательские сценарии ]**

Изменений нет.