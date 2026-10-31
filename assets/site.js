/* Web Design CNY — shared page behavior: menu, language switcher, scroll effects, phone demo, price builder, request form. */
(function(){
  var root = document.documentElement;
  var LANGS = window.WDC_LANGS || [{code:"en", name:"English", sub:""}];
  var DICT = window.WDC_I18N || {};
  var RTL = {ar:1, fa:1, ur:1, he:1};
  var lang = "en";
  function store(k, v){ try { if (v === undefined) return localStorage.getItem(k); localStorage.setItem(k, v); } catch(e) { return null; } }
  function t(key, en){ var d = DICT[lang]; return (d && d[key]) || en; }
  function fmt(s, n){ return s.replace("{n}", n); }

  /* ---------- mobile menu ---------- */
  var menuBtn = document.querySelector(".menu-btn"), nav = document.getElementById("nav");
  if (menuBtn && nav) menuBtn.addEventListener("click", function(){
    var open = nav.classList.toggle("open");
    menuBtn.setAttribute("aria-expanded", open ? "true" : "false");
  });

  /* ---------- language switcher ---------- */
  var langBox = document.getElementById("lang");
  function applyLang(code){
    lang = DICT[code] || code === "en" ? code : "en";
    root.lang = lang;
    root.dir = RTL[lang] ? "rtl" : "ltr";
    document.querySelectorAll("[data-i18n]").forEach(function(el){
      if (el.dataset.en === undefined) el.dataset.en = el.innerHTML;
      var v = lang === "en" ? null : DICT[lang][el.dataset.i18n];
      el.innerHTML = v || el.dataset.en;
    });
    document.querySelectorAll("[data-i18n-ph]").forEach(function(el){
      if (el.dataset.enPh === undefined) el.dataset.enPh = el.getAttribute("placeholder") || "";
      var v = lang === "en" ? null : DICT[lang][el.dataset.i18nPh];
      el.setAttribute("placeholder", v || el.dataset.enPh);
    });
    if (langBox) {
      var cur = LANGS.filter(function(l){ return l.code === lang; })[0] || LANGS[0];
      langBox.querySelector(".lname").textContent = cur.name;
      langBox.querySelectorAll("[role=menuitemradio]").forEach(function(b){ b.setAttribute("aria-checked", b.dataset.code === lang ? "true" : "false"); });
    }
    store("wdc-lang", lang);
    document.dispatchEvent(new CustomEvent("wdc:lang"));
  }
  if (langBox) {
    var menu = langBox.querySelector(".lang-menu"), btn = langBox.querySelector(".lang-btn");
    LANGS.forEach(function(l){
      var b = document.createElement("button");
      b.type = "button"; b.setAttribute("role", "menuitemradio"); b.dataset.code = l.code; b.lang = l.code;
      b.innerHTML = "<span></span><small></small>";
      b.firstChild.textContent = l.name; b.lastChild.textContent = l.sub || "";
      b.addEventListener("click", function(){ applyLang(l.code); langBox.classList.remove("open"); btn.setAttribute("aria-expanded", "false"); });
      menu.appendChild(b);
    });
    var note = document.createElement("p"); note.className = "note";
    note.textContent = "Translations are machine-assisted. More languages coming soon.";
    menu.appendChild(note);
    btn.addEventListener("click", function(e){
      e.stopPropagation();
      var open = langBox.classList.toggle("open");
      btn.setAttribute("aria-expanded", open ? "true" : "false");
    });
    document.addEventListener("click", function(e){ if (!langBox.contains(e.target)) { langBox.classList.remove("open"); btn.setAttribute("aria-expanded", "false"); } });
    document.addEventListener("keydown", function(e){ if (e.key === "Escape") { langBox.classList.remove("open"); btn.setAttribute("aria-expanded", "false"); } });
  }

  /* ---------- scroll: reveal sections, float stickers away ---------- */
  var reduce = window.matchMedia && window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  var reveals = document.querySelectorAll(".reveal");
  if ("IntersectionObserver" in window && !reduce) {
    var io = new IntersectionObserver(function(entries){
      entries.forEach(function(en){ if (en.isIntersecting) { en.target.classList.add("in"); io.unobserve(en.target); } });
    }, {rootMargin: "0px 0px -8% 0px", threshold: 0.08});
    reveals.forEach(function(el){ io.observe(el); });
  } else {
    reveals.forEach(function(el){ el.classList.add("in"); });
  }
  var scene = document.getElementById("scene");
  if (scene && !reduce) {
    var ticking = false;
    var update = function(){
      var r = scene.getBoundingClientRect();
      var p = Math.min(1, Math.max(0, -r.top / (r.height * 0.75) + 0.12));
      scene.style.setProperty("--p", p.toFixed(3));
      ticking = false;
    };
    window.addEventListener("scroll", function(){ if (!ticking) { ticking = true; requestAnimationFrame(update); } }, {passive: true});
    update();
  }

  /* ---------- phone demo ---------- */
  var phone = document.getElementById("phone");
  if (phone) {
    var kinds = {
      deli:   {acc:"#0E8A7E", ink:"#fff", name:"Your Deli", head:"Hot subs, pizza & groceries", sub:"Your corner deli. Order ahead or stop by.", btn:"Call to order", photo:"Your food photo",
               rows:[["d.mf","Mon–Fri","8 AM – 10 PM"],["d.sat","Sat","9 AM – 10 PM"],["d.sun","Sun","9 AM – 8 PM"]]},
      barber: {acc:"#1D1A33", ink:"#FFC23D", name:"Your Barbershop", head:"Fresh cuts. Walk-ins welcome.", sub:"Fades, beard trims and kids' cuts.", btn:"Book a chair", photo:"Your best cut",
               rows:[["d.r.haircut","Haircut","$25"],["d.r.fade","Fade + beard","$35"],["d.r.kids","Kids' cut","$18"]]},
      auto:   {acc:"#EE5236", ink:"#fff", name:"Your Auto Shop", head:"Honest repairs, done right", sub:"Brakes, oil changes, tires and inspections.", btn:"Call for a quote", photo:"Your garage",
               rows:[["d.mf","Mon–Fri","8 AM – 6 PM"],["d.sat","Sat","8 AM – 1 PM"],["d.sun","Sun",["d.closed","Closed"]]]},
      salon:  {acc:"#6D4AA8", ink:"#fff", name:"Your Salon", head:"Color, cuts & styling", sub:"Book your spot in under a minute.", btn:"Book now", photo:"Your work",
               rows:[["d.r.cut","Cut & style","$40"],["d.r.color","Color",["d.from","from","$75"]],["d.r.blow","Blowout","$30"]]},
      hustle: {acc:"#FFC23D", ink:"#1D1A33", name:"Your Name · Cleaning", head:"Home cleaning you can count on", sub:"Weekly, every two weeks or one time.", btn:"Text me for a quote", photo:"Before & after",
               rows:[["d.r.apt","Apartment",["d.from","from","$90"]],["d.r.house","House",["d.from","from","$130"]],["d.r.move","Move-out",["d.ask","Ask"]]]}
    };
    var current = "deli";
    var val = function(v){ if (typeof v === "string") return v; return v.length === 3 ? t(v[0], v[1]) + " " + v[2] : t(v[0], v[1]); };
    var fill = function(k){
      var d = kinds[k];
      phone.style.setProperty("--acc", d.acc);
      phone.style.setProperty("--acc-ink", d.ink);
      ["name","head","sub","btn","photo"].forEach(function(f){ phone.querySelector('[data-f="' + f + '"]').textContent = t("d." + k + "." + f, d[f]); });
      var rows = phone.querySelector('[data-f="rows"]');
      rows.textContent = "";
      d.rows.forEach(function(r){
        var b = document.createElement("b"); b.textContent = t(r[0], r[1]);
        var s = document.createElement("span"); s.textContent = val(r[2]);
        rows.appendChild(b); rows.appendChild(s);
      });
    };
    var chips = document.querySelectorAll(".chip");
    var show = function(k){
      current = k;
      chips.forEach(function(c){ c.setAttribute("aria-pressed", c.dataset.kind === k ? "true" : "false"); });
      if (reduce) { fill(k); return; }
      phone.classList.add("is-swapping");
      setTimeout(function(){ fill(k); phone.classList.remove("is-swapping"); }, 200);
    };
    chips.forEach(function(c){ c.addEventListener("click", function(){ show(c.dataset.kind); }); });
    document.addEventListener("wdc:lang", function(){ fill(current); });
  }

  /* ---------- build your own ---------- */
  var boxes = Array.prototype.slice.call(document.querySelectorAll(".opts input[type=checkbox]"));
  var calc = null;
  if (boxes.length) {
    var linesEl = document.getElementById("lines"), totalEl = document.getElementById("total"), tipEl = document.getElementById("tip");
    var hustler = ["onepage","gprofile","flyer","card"], entre = ["site","gclean","qr","flyer","card"];
    var nameOf = function(b){ return b.parentNode.querySelector("b").textContent; };
    var within = function(sel, set){ return sel.every(function(b){ return set.indexOf(b.value) > -1; }); };
    calc = function(){
      var sel = boxes.filter(function(b){ return b.checked; }), total = 0, has = {};
      sel.forEach(function(b){ total += +b.dataset.price; has[b.value] = 1; });
      var combo = has.flyer && has.card;
      if (combo) total -= 5;
      linesEl.textContent = "";
      if (!sel.length) { var e = document.createElement("span"); e.className = "empty"; e.textContent = t("js.empty", "Nothing picked yet."); linesEl.appendChild(e); }
      var row = function(a, b){ var r = document.createElement("div"), x = document.createElement("span"), y = document.createElement("span"); x.textContent = a; y.textContent = b; r.appendChild(x); r.appendChild(y); linesEl.appendChild(r); };
      sel.forEach(function(b){ row(nameOf(b), "$" + b.dataset.price); });
      if (combo) row(t("js.combo", "Flyer + card together"), "−$5");
      totalEl.textContent = "$" + total;
      var tip = "";
      if (sel.length && within(sel, hustler) && total > 150) tip = fmt(t("js.tipH", "The Hustler package includes all of this for $150. You'd save ${n}."), total - 150);
      else if (sel.length && within(sel, entre) && total > 300) tip = fmt(t("js.tipE", "The Entrepreneur package includes all of this for $300. You'd save ${n}."), total - 300);
      else if (has.site && has.onepage) tip = t("js.tipBoth", "You only need one website. The one-page site is for side hustles; the full site is for shops.");
      tipEl.textContent = tip; tipEl.hidden = !tip;
      return {sel: sel, total: total};
    };
    boxes.forEach(function(b){ b.addEventListener("change", calc); });
    document.addEventListener("wdc:lang", calc);
    calc();
    document.getElementById("build-cta").addEventListener("click", function(ev){
      var r = calc();
      if (!r.sel.length) return;
      ev.preventDefault();
      var picked = r.sel.map(function(b){ return b.value; }).join(",");
      location.href = "contact.html?plan=custom&items=" + encodeURIComponent(picked);
    });
  }

  /* ---------- contact form ---------- */
  var form = document.getElementById("sample-form");
  if (form) {
    var q = new URLSearchParams(location.search);
    var planSel = form.elements.plan;
    if (q.get("plan")) for (var i = 0; i < planSel.options.length; i++) if (planSel.options[i].value === q.get("plan")) planSel.selectedIndex = i;
    var items = q.get("items");
    var names = {site:"Small business website", onepage:'One-page "hire me" site', gprofile:"Google profile setup", gclean:"Google listing cleanup", qr:"Review QR card design", flyer:"Flyer design", card:"Business card design"};
    var prices = {site:200, onepage:100, gprofile:50, gclean:75, qr:35, flyer:30, card:25};
    var fillItems = function(){
      if (!items) return;
      var list = items.split(",").filter(function(k){ return names[k]; });
      var tot = list.reduce(function(s, k){ return s + prices[k]; }, 0) - (list.indexOf("flyer") > -1 && list.indexOf("card") > -1 ? 5 : 0);
      form.elements.note.value = t("js.noteprefix", "I'm interested in: ") + list.map(function(k){ return names[k]; }).join(", ") + " ($" + tot + ")";
    };
    fillItems();
    form.addEventListener("submit", function(ev){
      ev.preventDefault();
      var v = function(n){ var el = form.elements[n]; if (el.tagName === "SELECT") return el.options[el.selectedIndex].text; return (el.value || "").trim(); };
      var body = [
        t("js.mail.hi", "Hi David,"), "",
        t("js.mail.want", "I'd like a free sample for my business."), "",
        t("js.mail.biz", "Business") + ": " + v("business"),
        t("js.mail.type", "Type") + ": " + v("kind"),
        t("js.mail.name", "My name") + ": " + v("name"),
        t("js.mail.reach", "Best way to reach me") + ": " + v("reach"),
        t("js.mail.plan", "Interested in") + ": " + v("plan")
      ];
      if (v("note")) body.push("", v("note"));
      if (lang !== "en") body.push("", "(Language: " + lang + ")");
      location.href = "mailto:david@webdesigncny.com?subject=" + encodeURIComponent(t("js.mail.subj", "Free sample") + ": " + v("business")) + "&body=" + encodeURIComponent(body.join("\n"));
    });
  }

  /* ---------- start in the saved language ---------- */
  var saved = store("wdc-lang");
  if (saved && saved !== "en" && DICT[saved]) applyLang(saved);
  else if (langBox) langBox.querySelectorAll("[role=menuitemradio]").forEach(function(b){ b.setAttribute("aria-checked", b.dataset.code === "en" ? "true" : "false"); });
})();
