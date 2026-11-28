/* ODIRAH concept site: shared behaviour for every page. */
(function(){
  var root=document.documentElement; root.classList.add('js');
  var B=root.getAttribute('data-base')||'';
  var reduce=window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  var esc=function(s){return String(s).replace(/&/g,'&amp;').replace(/</g,'&lt;');};
  var $=function(s,c){return (c||document).querySelector(s);};
  var $$=function(s,c){return [].slice.call((c||document).querySelectorAll(s));};

  var ARCH=[
    {id:'silk-and-ashes',n:'I',arch:'The Maiden',name:'Silk & Ashes',story:'Silver morning light on silk. The self before the world arrived.',tone:'#EDE5E1'},
    {id:'skin-and-shadow',n:'II',arch:'The Lover',name:'Skin & Shadow',story:'Warm skin, a shadow on the wall, the hour no one else sees.',tone:'#E8DCD2'},
    {id:'ember-and-desire',n:'III',arch:'The Seductress',name:'Ember & Desire',story:'Velvet, ember and a mirror that keeps your secret.',tone:'#EBD9D3'},
    {id:'stars-and-whisper',n:'IV',arch:'The Wanderer',name:'Stars & Whisper',story:'A tent of light under the open sky. Home is where you breathe.',tone:'#E4E0E2'},
    {id:'velvet-and-poise',n:'V',arch:'The Queen',name:'Velvet & Poise',story:'Stillness, gold, and a key she has always held.',tone:'#E9E0DD'},
    {id:'rain-and-solace',n:'VI',arch:'The Healer',name:'Rain & Solace',story:'Rain on old stone. The quiet that puts you back together.',tone:'#E5E4DA'}
  ];
  var PRODUCTS={kit:{name:'Discovery Kit',meta:'6 × 7/10 ml · all six',img:B+'assets/img/discovery-kit-800.webp',script:false}};
  ARCH.forEach(function(a){PRODUCTS[a.id]={name:a.name,meta:'100 ml · '+a.arch,img:B+'assets/img/'+a.id+'-640.webp',script:true};});

  /* ---------- product tiles ---------- */
  function tile(a,sizes){
    return '<article class="panel tile" data-type="fragrance" style="--tone:'+a.tone+'">'+
      '<div class="tile-top"><span class="label">'+a.n+'</span></div>'+
      '<a class="arch" href="'+B+'fragrances/'+a.id+'.html" aria-label="'+esc(a.name)+', '+a.arch+'"><img src="'+B+'assets/img/'+a.id+'-640.webp" srcset="'+B+'assets/img/'+a.id+'-640.webp 640w, '+B+'assets/img/'+a.id+'-1200.webp 1200w" sizes="'+(sizes||'(max-width:600px) 52vw, (max-width:1060px) 30vw, 20vw')+'" width="1200" height="1490" loading="lazy" decoding="async" alt="Painterly illustration of '+a.arch+'’s world for '+esc(a.name)+'."></a>'+
      '<div class="tile-name"><h3><a href="'+B+'fragrances/'+a.id+'.html" style="text-decoration:none">'+esc(a.name)+'</a></h3><span class="vol">100 ml</span></div>'+
      '<p class="arch-name label">'+a.arch+'</p>'+
      '<p class="story">'+a.story+'</p>'+
      '<button type="button" class="add" data-add="'+a.id+'">Add to bag</button></article>';
  }
  function kitTile(){
    return '<article class="panel tile span2" data-type="kit" style="--tone:#E6DAD3">'+
      '<div class="tile-top"><span class="label">I–VI</span></div>'+
      '<a class="arch" href="'+B+'discovery-kit.html" aria-label="Discovery Kit"><img src="'+B+'assets/img/discovery-kit-800.webp" width="800" height="600" loading="lazy" decoding="async" alt="The Discovery Kit box with six vials."></a>'+
      '<div class="tile-name"><h3 style="font-family:var(--f-serif);font-weight:500;font-size:clamp(1.8rem,1.4rem + 1vw,2.4rem)"><a href="'+B+'discovery-kit.html" style="text-decoration:none">Discovery Kit</a></h3><span class="vol">6 × 7/10 ml</span></div>'+
      '<p class="arch-name label">All six archetypes</p>'+
      '<p class="story">Meet all six before you choose a full size.</p>'+
      '<button type="button" class="add" data-add="kit">Add to bag</button></article>';
  }
  $$('[data-tiles]').forEach(function(el){
    var ex=el.getAttribute('data-exclude'), sizes=el.getAttribute('data-sizes');
    var html=ARCH.filter(function(a){return a.id!==ex;}).map(function(a){return tile(a,sizes);}).join('');
    if(el.hasAttribute('data-with-kit')) html+=kitTile();
    el.innerHTML=html;
  });

  /* ---------- shop filters ---------- */
  var chips=$$('[data-filter]');
  chips.forEach(function(c){c.addEventListener('click',function(){
    var f=c.getAttribute('data-filter');
    chips.forEach(function(x){x.setAttribute('aria-pressed',x===c);});
    $$('.tile').forEach(function(t){t.hidden=!(f==='all'||t.getAttribute('data-type')===f);});
  });});

  /* ---------- header ---------- */
  var header=$('.site-header'), hero=$('.hero');
  if(hero){
    var onScroll=function(){header.classList.toggle('is-solid',window.scrollY>hero.offsetHeight-84);};
    onScroll(); window.addEventListener('scroll',onScroll,{passive:true});
  }

  /* ---------- hero film ---------- */
  var film=$('[data-film]'), ft=$('[data-film-toggle]');
  var saveData=navigator.connection&&navigator.connection.saveData;
  if(film&&!reduce&&!saveData){
    if(window.matchMedia('(max-width: 900px)').matches&&film.dataset.srcSmall){film.innerHTML='<source src="'+film.dataset.srcSmall+'" type="video/mp4">';}
    film.preload='auto'; film.load();
    film.addEventListener('playing',function(){film.classList.add('is-playing');if(ft)ft.hidden=false;},{once:true});
    var pr=film.play(); if(pr&&pr.catch)pr.catch(function(){});
    if(ft)ft.addEventListener('click',function(){
      var paused=!film.paused; if(paused)film.pause(); else film.play();
      ft.setAttribute('aria-pressed',paused);
      $('[data-film-label]').textContent=paused?'Play film':'Pause film';
      $('[data-icon]',ft).setAttribute('d',paused?'M1 0l7 4-7 4z':'M1 0h2v8H1zM5 0h2v8H5z');
    });
  } else if(film){film.remove();}

  /* ---------- reveal ---------- */
  var els=$$('.reveal');
  if(reduce||!('IntersectionObserver' in window)){els.forEach(function(el){el.classList.add('in');});}
  else{
    var io=new IntersectionObserver(function(entries){entries.forEach(function(en){if(en.isIntersecting){var el=en.target;var sib=[].slice.call(el.parentNode.children).filter(function(x){return x.classList.contains('reveal');});el.style.transitionDelay=Math.min(sib.indexOf(el),4)*110+'ms';el.classList.add('in');io.unobserve(el);}});},{rootMargin:'0px 0px -6% 0px',threshold:.06});
    els.forEach(function(el){io.observe(el);});
    setTimeout(function(){els.forEach(function(el){el.classList.add('in');});},4000);
  }

  /* ---------- menu ---------- */
  var menu=$('#menu'), menuBtn=$('[data-open-menu]');
  function setMenu(open){if(!menu)return;menu.classList.toggle('is-open',open);menuBtn.setAttribute('aria-expanded',open);document.body.style.overflow=open?'hidden':'';if(open)$('[data-close-menu]',menu).focus();}
  if(menuBtn)menuBtn.addEventListener('click',function(){setMenu(true);});
  if(menu)menu.addEventListener('click',function(e){if(e.target.closest('[data-close-menu]'))setMenu(false);});

  /* ---------- toast ---------- */
  var toastEl=document.createElement('div'); toastEl.className='toast'; toastEl.setAttribute('role','status'); document.body.appendChild(toastEl);
  var tt; function toast(msg){toastEl.textContent=msg;toastEl.classList.add('is-on');clearTimeout(tt);tt=setTimeout(function(){toastEl.classList.remove('is-on');},2600);}

  /* ---------- bag (kept in this browser across pages) ---------- */
  var KEY='odirah-bag', cart={};
  try{cart=JSON.parse(localStorage.getItem(KEY)||'{}')||{};}catch(e){cart={};}
  Object.keys(cart).forEach(function(k){if(!PRODUCTS[k]||!(cart[k]>0))delete cart[k];});
  function save(){try{localStorage.setItem(KEY,JSON.stringify(cart));}catch(e){}}
  var bag=$('#bag'), scrim=$('[data-scrim]'), itemsEl=$('[data-items]'), lastFocus=null;
  function render(){
    var ids=Object.keys(cart), total=ids.reduce(function(s,k){return s+cart[k];},0);
    $$('[data-count]').forEach(function(c){c.textContent=total;});
    if(!itemsEl)return;
    itemsEl.innerHTML=ids.length?ids.map(function(id){var p=PRODUCTS[id];return '<div class="line-item"><img src="'+p.img+'" alt=""><div><div class="'+(p.script?'script':'label')+'">'+esc(p.name)+'</div><div class="qty"><button type="button" aria-label="Remove one '+esc(p.name)+'" data-dec="'+id+'">−</button><span>'+cart[id]+'</span><button type="button" aria-label="Add one '+esc(p.name)+'" data-inc="'+id+'">+</button></div><div style="font-size:.9rem;color:var(--brown)">'+p.meta+'</div></div><button type="button" class="remove" data-remove="'+id+'">Remove</button></div>';}).join(''):'<p class="empty">Your bag is empty. Begin with the archetype you recognise.</p>';
  }
  function setBag(open){if(!bag)return;bag.classList.toggle('is-open',open);scrim.classList.toggle('is-open',open);document.body.style.overflow=open?'hidden':'';if(open){lastFocus=document.activeElement;$('[data-close-bag]',bag).focus();}else if(lastFocus){lastFocus.focus();}}
  document.addEventListener('click',function(e){
    var t=e.target;
    var add=t.closest('[data-add]');
    if(add){var id=add.getAttribute('data-add');cart[id]=(cart[id]||0)+1;save();render();setMenu(false);setBag(true);return;}
    if(t.closest('[data-open-bag]')){e.preventDefault();setMenu(false);setBag(true);return;}
    if(t.closest('[data-close-bag]')||t===scrim){setBag(false);return;}
    var x;
    if((x=t.closest('[data-inc]'))){cart[x.getAttribute('data-inc')]++;save();render();return;}
    if((x=t.closest('[data-dec]'))){var k=x.getAttribute('data-dec');cart[k]--;if(cart[k]<=0)delete cart[k];save();render();return;}
    if((x=t.closest('[data-remove]'))){delete cart[x.getAttribute('data-remove')];save();render();return;}
    if(t.closest('[data-checkout]')){$('[data-checkout-msg]').textContent='In the live site this opens Shopify checkout.';return;}
    if((x=t.closest('[data-soon]'))){e.preventDefault();toast(x.getAttribute('data-soon'));return;}
    if((x=t.closest('[data-copy]'))){var v=x.getAttribute('data-copy');
      var done=function(){toast('Copied '+v);};
      if(navigator.clipboard&&navigator.clipboard.writeText){navigator.clipboard.writeText(v).then(done,function(){toast(v);});}else{toast(v);}
    }
  });
  document.addEventListener('keydown',function(e){if(e.key==='Escape'){setBag(false);setMenu(false);}});
  render();

  /* ---------- sticky add bar on product pages ---------- */
  var sticky=$('[data-sticky-buy]'), mainAdd=$('[data-main-add]');
  if(sticky&&mainAdd){
    var checkSticky=function(){sticky.classList.toggle('is-on',mainAdd.getBoundingClientRect().bottom<0);};
    checkSticky(); window.addEventListener('scroll',checkSticky,{passive:true});
  }

  /* ---------- forms (concept: nothing is sent) ---------- */
  var okEmail=function(v){return /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(v);};
  $$('[data-news]').forEach(function(f){f.addEventListener('submit',function(e){e.preventDefault();var v=$('input[type=email]',f).value.trim();var m=f.parentNode.querySelector('[data-news-msg]');m.textContent=okEmail(v)?'Thank you. The first letter will find you soon.':'Please enter a valid email address.';});});
  var cf=$('[data-contact]');
  if(cf)cf.addEventListener('submit',function(e){e.preventDefault();var m=$('[data-contact-msg]',cf);var em=$('#c-email',cf).value.trim(), msg=$('#c-message',cf).value.trim();
    if(!okEmail(em)){m.textContent='Please enter a valid email address so we can reply.';return;}
    if(!msg){m.textContent='Please write a short message.';return;}
    m.textContent='Thank you. In the live site this message goes to the house; this preview does not send it.';cf.reset();});
})();
