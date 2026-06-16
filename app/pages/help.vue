<script setup lang="ts">
import {
  FileText, Plus, Filter, ChevronDown, Pencil, Truck, Users,
  Car, ClipboardList, CheckCircle, Info, AlertCircle
} from 'lucide-vue-next'
</script>

<template>
  <div>
    <h2 class="text-3xl font-bold mb-6">Инструкция по работе</h2>

    <Tabs value="manager">
      <TabList>
        <Tab value="manager">Менеджер</Tab>
        <Tab value="logist">Логист</Tab>
      </TabList>

      <TabPanels>

        <!-- ========== МЕНЕДЖЕР ========== -->
        <TabPanel value="manager">
          <div class="flex flex-col gap-6 mt-4">

            <!-- Раздел: Заявки -->
            <div>
              <div class="flex items-center gap-2 mb-3">
                <FileText class="text-primary" :size="20"/>
                <h3 class="text-xl font-bold">Раздел «Заявки»</h3>
              </div>

              <div class="flex flex-col gap-3">
                <Card>
                  <template #content>
                    <div class="flex gap-3">
                      <span class="flex-shrink-0 w-7 h-7 rounded-full flex items-center justify-center text-white text-sm font-bold"
                            style="background: linear-gradient(135deg, #00d8a5, #8cd66a)">1</span>
                      <div>
                        <p class="font-semibold mb-1">Создание накладной</p>
                        <p class="text-sm text-muted-foreground">Нажмите кнопку <strong>«Создать заявку»</strong> в правом верхнем углу страницы.</p>
                        <ul class="text-sm text-muted-foreground mt-2 list-disc list-inside space-y-1">
                          <li>Выберите <strong>организацию</strong> из списка</li>
                          <li>Выберите <strong>спецификацию</strong> (договор с условиями)</li>
                          <li>Укажите <strong>условие оплаты</strong>: Предоплата, Отсрочка платежа или Лимит</li>
                          <li>Укажите <strong>адрес доставки</strong></li>
                        </ul>
                      </div>
                    </div>
                  </template>
                </Card>

                <Card>
                  <template #content>
                    <div class="flex gap-3">
                      <span class="flex-shrink-0 w-7 h-7 rounded-full flex items-center justify-center text-white text-sm font-bold"
                            style="background: linear-gradient(135deg, #00d8a5, #8cd66a)">2</span>
                      <div>
                        <p class="font-semibold mb-1">Фильтрация списка заявок</p>
                        <p class="text-sm text-muted-foreground">Используйте фильтры вверху страницы:</p>
                        <ul class="text-sm text-muted-foreground mt-2 list-disc list-inside space-y-1">
                          <li><strong>Источник</strong> (Ресурс / Неруд-Трейд) — фильтрует по базе 1С</li>
                          <li><strong>Организация</strong> — выбор конкретного контрагента</li>
                          <li><strong>Поиск</strong> — по номеру накладной</li>
                          <li><strong>Статус</strong>: Все заявки / Открытые / История отгрузок</li>
                        </ul>
                      </div>
                    </div>
                  </template>
                </Card>

                <Card>
                  <template #content>
                    <div class="flex gap-3">
                      <span class="flex-shrink-0 w-7 h-7 rounded-full flex items-center justify-center text-white text-sm font-bold"
                            style="background: linear-gradient(135deg, #00d8a5, #8cd66a)">3</span>
                      <div>
                        <p class="font-semibold mb-1">Редактирование накладной</p>
                        <p class="text-sm text-muted-foreground">
                          Нажмите кнопку <strong>карандаш</strong> в строке нужной заявки. Откроется форма редактирования с теми же полями.
                        </p>
                      </div>
                    </div>
                  </template>
                </Card>

                <Card>
                  <template #content>
                    <div class="flex gap-3">
                      <span class="flex-shrink-0 w-7 h-7 rounded-full flex items-center justify-center text-white text-sm font-bold"
                            style="background: linear-gradient(135deg, #00d8a5, #8cd66a)">4</span>
                      <div>
                        <p class="font-semibold mb-1">Статусы накладных</p>
                        <div class="flex flex-wrap gap-2 mt-2">
                          <Tag value="Принято" severity="info"/>
                          <Tag value="В обработке" severity="warn"/>
                          <Tag value="Успешно" severity="success"/>
                          <Tag value="Отклонено" severity="danger"/>
                        </div>
                        <p class="text-sm text-muted-foreground mt-2">Статус обновляется логистом по мере работы с заказами.</p>
                      </div>
                    </div>
                  </template>
                </Card>
              </div>
            </div>

            <!-- Раздел: Служебные авто -->
            <div>
              <div class="flex items-center gap-2 mb-3">
                <Car class="text-primary" :size="20"/>
                <h3 class="text-xl font-bold">Раздел «Служебные авто»</h3>
              </div>

              <div class="flex flex-col gap-3">
                <Card>
                  <template #content>
                    <div class="flex gap-3">
                      <span class="flex-shrink-0 w-7 h-7 rounded-full flex items-center justify-center text-white text-sm font-bold"
                            style="background: linear-gradient(135deg, #00d8a5, #8cd66a)">1</span>
                      <div>
                        <p class="font-semibold mb-1">Что такое служебные авто</p>
                        <p class="text-sm text-muted-foreground">
                          Машины, которые въезжают на территорию карьера, но <strong>не участвуют в заказах</strong> (не отгружают материалы). Например, служебный транспорт, технические машины.
                        </p>
                      </div>
                    </div>
                  </template>
                </Card>

                <Card>
                  <template #content>
                    <div class="flex gap-3">
                      <span class="flex-shrink-0 w-7 h-7 rounded-full flex items-center justify-center text-white text-sm font-bold"
                            style="background: linear-gradient(135deg, #00d8a5, #8cd66a)">2</span>
                      <div>
                        <p class="font-semibold mb-1">Добавление служебного авто</p>
                        <p class="text-sm text-muted-foreground">Нажмите <strong>«Добавить авто»</strong>. Заполните:</p>
                        <ul class="text-sm text-muted-foreground mt-2 list-disc list-inside space-y-1">
                          <li><strong>Гос. номер</strong> — только латинские буквы и цифры (вводится автоматически заглавными)</li>
                          <li><strong>Марка</strong> и <strong>Модель</strong></li>
                          <li><strong>Фото</strong> — нажмите на область с изображением</li>
                        </ul>
                      </div>
                    </div>
                  </template>
                </Card>

                <Card>
                  <template #content>
                    <div class="flex gap-3">
                      <span class="flex-shrink-0 w-7 h-7 rounded-full flex items-center justify-center text-white text-sm font-bold"
                            style="background: linear-gradient(135deg, #00d8a5, #8cd66a)">3</span>
                      <div>
                        <p class="font-semibold mb-1">Удаление служебного авто</p>
                        <p class="text-sm text-muted-foreground">
                          Откройте карточку авто (кнопка карандаш) и нажмите красную кнопку <strong>«Удалить»</strong>.
                        </p>
                      </div>
                    </div>
                  </template>
                </Card>
              </div>
            </div>

          </div>
        </TabPanel>

        <!-- ========== ЛОГИСТ ========== -->
        <TabPanel value="logist">
          <div class="flex flex-col gap-6 mt-4">

            <!-- Раздел: Работа с заказами -->
            <div>
              <div class="flex items-center gap-2 mb-3">
                <ClipboardList class="text-primary" :size="20"/>
                <h3 class="text-xl font-bold">Работа с заказами</h3>
              </div>

              <div class="flex flex-col gap-3">
                <Card>
                  <template #content>
                    <div class="flex gap-3">
                      <span class="flex-shrink-0 w-7 h-7 rounded-full flex items-center justify-center text-white text-sm font-bold"
                            style="background: linear-gradient(135deg, #00d8a5, #8cd66a)">1</span>
                      <div>
                        <p class="font-semibold mb-1">Раскрыть накладную</p>
                        <p class="text-sm text-muted-foreground">
                          На странице <strong>«Заявки»</strong> нажмите на стрелку <strong>▶</strong> слева от строки накладной — развернётся список заказов по ней.
                        </p>
                      </div>
                    </div>
                  </template>
                </Card>

                <Card>
                  <template #content>
                    <div class="flex gap-3">
                      <span class="flex-shrink-0 w-7 h-7 rounded-full flex items-center justify-center text-white text-sm font-bold"
                            style="background: linear-gradient(135deg, #00d8a5, #8cd66a)">2</span>
                      <div>
                        <p class="font-semibold mb-1">Создание заказа</p>
                        <p class="text-sm text-muted-foreground">Нажмите <strong>«Добавить заказ»</strong> внутри накладной. Заполните форму:</p>
                        <ul class="text-sm text-muted-foreground mt-2 list-disc list-inside space-y-1">
                          <li><strong>Машина</strong> — показываются только машины из той же базы 1С, что и организация накладной</li>
                          <li><strong>Водитель</strong> — аналогично, только из нужной базы</li>
                          <li><strong>Номенклатура</strong> — материал для отгрузки (из спецификации)</li>
                          <li><strong>Количество на отгрузку</strong></li>
                          <li><strong>Адрес поставки</strong></li>
                          <li><strong>Комментарий</strong> — при необходимости</li>
                        </ul>
                      </div>
                    </div>
                  </template>
                </Card>

                <Card>
                  <template #content>
                    <div class="flex gap-3">
                      <span class="flex-shrink-0 w-7 h-7 rounded-full flex items-center justify-center text-white text-sm font-bold"
                            style="background: linear-gradient(135deg, #00d8a5, #8cd66a)">3</span>
                      <div>
                        <p class="font-semibold mb-1">Жизненный цикл заказа</p>
                        <div class="flex flex-col gap-2 mt-2 text-sm text-muted-foreground">
                          <div class="flex items-start gap-2">
                            <CheckCircle class="text-green-500 flex-shrink-0 mt-0.5" :size="16"/>
                            <span>Заказ создан — ожидает назначения на карьер-сервере</span>
                          </div>
                          <div class="flex items-start gap-2">
                            <CheckCircle class="text-green-500 flex-shrink-0 mt-0.5" :size="16"/>
                            <span>Карьер-сервер автоматически забирает заказ и назначает водителю</span>
                          </div>
                          <div class="flex items-start gap-2">
                            <CheckCircle class="text-green-500 flex-shrink-0 mt-0.5" :size="16"/>
                            <span>После отгрузки карьер-сервер присылает <strong>факт</strong> — фактический объём</span>
                          </div>
                          <div class="flex items-start gap-2">
                            <CheckCircle class="text-green-500 flex-shrink-0 mt-0.5" :size="16"/>
                            <span>Заказ помечается <strong>«Отгружен»</strong>, данные автоматически уходят в 1С</span>
                          </div>
                        </div>
                      </div>
                    </div>
                  </template>
                </Card>

                <Card>
                  <template #content>
                    <div class="flex gap-3">
                      <AlertCircle class="text-orange-400 flex-shrink-0 mt-0.5" :size="20"/>
                      <div>
                        <p class="font-semibold mb-1">Важно</p>
                        <p class="text-sm text-muted-foreground">
                          Редактирование заказа недоступно после того как он отмечен <strong>«Отгружен»</strong>. Все поля формы будут заблокированы.
                        </p>
                      </div>
                    </div>
                  </template>
                </Card>
              </div>
            </div>

            <!-- Раздел: Водители -->
            <div>
              <div class="flex items-center gap-2 mb-3">
                <Users class="text-primary" :size="20"/>
                <h3 class="text-xl font-bold">Раздел «Водители»</h3>
              </div>

              <div class="flex flex-col gap-3">
                <Card>
                  <template #content>
                    <div class="flex gap-3">
                      <span class="flex-shrink-0 w-7 h-7 rounded-full flex items-center justify-center text-white text-sm font-bold"
                            style="background: linear-gradient(135deg, #00d8a5, #8cd66a)">1</span>
                      <div>
                        <p class="font-semibold mb-1">Просмотр водителей</p>
                        <p class="text-sm text-muted-foreground">
                          Водители разделены по двум базам 1С. Нажмите на секцию <strong>«Ресурс»</strong> или <strong>«Неруд-Трейд»</strong> чтобы развернуть список.
                        </p>
                      </div>
                    </div>
                  </template>
                </Card>

                <Card>
                  <template #content>
                    <div class="flex gap-3">
                      <span class="flex-shrink-0 w-7 h-7 rounded-full flex items-center justify-center text-white text-sm font-bold"
                            style="background: linear-gradient(135deg, #00d8a5, #8cd66a)">2</span>
                      <div>
                        <p class="font-semibold mb-1">Редактирование водителя</p>
                        <p class="text-sm text-muted-foreground">
                          Нажмите карандаш. <strong>Данные из 1С</strong> (ФИО, ИНН, телефон, права) — только для просмотра, изменить их нельзя. Доступно для редактирования:
                        </p>
                        <ul class="text-sm text-muted-foreground mt-2 list-disc list-inside space-y-1">
                          <li><strong>Telegram ID</strong> — для связи с водителем через карьер-сервер</li>
                          <li><strong>Фото</strong></li>
                        </ul>
                      </div>
                    </div>
                  </template>
                </Card>
              </div>
            </div>

            <!-- Раздел: Автомобили -->
            <div>
              <div class="flex items-center gap-2 mb-3">
                <Truck class="text-primary" :size="20"/>
                <h3 class="text-xl font-bold">Раздел «Автомобили»</h3>
              </div>

              <div class="flex flex-col gap-3">
                <Card>
                  <template #content>
                    <div class="flex gap-3">
                      <span class="flex-shrink-0 w-7 h-7 rounded-full flex items-center justify-center text-white text-sm font-bold"
                            style="background: linear-gradient(135deg, #00d8a5, #8cd66a)">1</span>
                      <div>
                        <p class="font-semibold mb-1">Просмотр машин</p>
                        <p class="text-sm text-muted-foreground">
                          Как и водители, машины разделены по базам 1С. Нажмите на секцию для раскрытия списка.
                        </p>
                      </div>
                    </div>
                  </template>
                </Card>

                <Card>
                  <template #content>
                    <div class="flex gap-3">
                      <span class="flex-shrink-0 w-7 h-7 rounded-full flex items-center justify-center text-white text-sm font-bold"
                            style="background: linear-gradient(135deg, #00d8a5, #8cd66a)">2</span>
                      <div>
                        <p class="font-semibold mb-1">Редактирование машины</p>
                        <p class="text-sm text-muted-foreground">
                          Нажмите карандаш. Данные из 1С (номер, марка, модель) — только для просмотра. Доступно для редактирования:
                        </p>
                        <ul class="text-sm text-muted-foreground mt-2 list-disc list-inside space-y-1">
                          <li><strong>Не взвешивать</strong> — флаг для машин, которые не нужно взвешивать на въезде</li>
                          <li><strong>Фото</strong></li>
                        </ul>
                      </div>
                    </div>
                  </template>
                </Card>
              </div>
            </div>

            <!-- Раздел: Служебные авто -->
            <div>
              <div class="flex items-center gap-2 mb-3">
                <Car class="text-primary" :size="20"/>
                <h3 class="text-xl font-bold">Раздел «Служебные авто»</h3>
              </div>
              <Card>
                <template #content>
                  <p class="text-sm text-muted-foreground">
                    Добавление, редактирование и удаление машин, которые въезжают на территорию карьера но не участвуют в отгрузке. Подробнее — см. инструкцию для менеджера.
                  </p>
                </template>
              </Card>
            </div>

          </div>
        </TabPanel>

      </TabPanels>
    </Tabs>
  </div>
</template>
