!function(l) {
    "use strict";
    function e() {
        this.$body = l("body"),
        this.$modal = new bootstrap.Modal(document.getElementById("event-modal"),{
            backdrop: "static"
        }),
        this.$calendar = l("#calendar"),
        this.$formEvent = l("#form-event"),
        this.$btnDeleteEvent = l("#btn-delete-event"),
        this.$modalTitle = l("#modal-title"),
        this.$calendarObj = null,
        this.$selectedEvent = null,
        this.$newEventData = null
    }
    e.prototype.onEventClick = function(e) {
        this.$newEventData = null,
        this.$btnDeleteEvent.show(),
        this.$modalTitle.text("Delete Weekend Day"),
        this.$modal.show(),
        this.$selectedEvent = e.event,
        this.$selectedID = e.event._def.publicId,
        l("#event-title").val(this.$selectedEvent.title),
        l("#event-category").val(this.$selectedEvent.classNames[0])
    }
    ,
    e.prototype.init = function() {
        var e = new Date(l.now());
        new FullCalendar.Draggable(document.getElementById("external-events"),{
            itemSelector: ".external-event",
            eventData: function(e) {
                return {
                    title: e.innerText,
                    className: l(e).data("class"),
                }
            }
        });

        var hub = $('#id_hub').text().slice(1, -1);
        var t = [], a = this;

        a.$calendarObj = new FullCalendar.Calendar(a.$calendar[0],{
            themeSystem: "bootstrap",
            bootstrapFontAwesome: !1,
            buttonText: {
                today: "Current Month",
                prev: "Prev",
                next: "Next",
            },
            firstDay: 1,
            initialView: "dayGridMonth",
            handleWindowResize: !0,
            height: l(window).height() - 200,
            headerToolbar: {
                left: "prev,next today",
                right: "title",

            },
            eventSources: [
                {url: "/ajax/weekend-working/" + hub + "/"}],
            editable: false,
            droppable: false,
            selectable: false,
            dateClick: false,
            eventClick: false,
        }),
        a.$calendarObj.render()
    }
    ,
    l.CalendarApp = new e,
    l.CalendarApp.Constructor = e
}(window.jQuery),
function() {
    "use strict";
    window.jQuery.CalendarApp.init()
}();
