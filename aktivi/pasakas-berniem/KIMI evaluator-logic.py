<!DOCTYPE html>
<html lang="lv">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>🧚 Pasaku Fabrika LIVE | Doodle Video Illustrations</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/html2pdf.js/0.10.1/html2pdf.bundle.min.js"></script>
    <script src="https://apis.google.com/js/api.js"></script>
    <link href="https://fonts.googleapis.com/css2?family=Cinzel:wght@400;600&family=Nunito:wght@300;400;600;700&family=Patrick+Hand&display=swap" rel="stylesheet">
    <style>
        body {
            font-family: 'Nunito', sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
        }
        .fairytale-font { font-family: 'Cinzel', serif; }
        .handwritten { font-family: 'Patrick Hand', cursive; }
        
        .glass-panel {
            background: rgba(255, 255, 255, 0.95);
            backdrop-filter: blur(10px);
            border: 1px solid rgba(255, 255, 255, 0.2);
        }
        .gradient-text {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }

        /* Doodle Animation Container */
        .doodle-container {
            position: relative;
            width: 100%;
            max-width: 600px;
            margin: 2rem auto;
            background: #fffef7;
            border-radius: 20px;
            box-shadow: 0 20px 60px rgba(0,0,0,0.15);
            overflow: hidden;
            border: 3px solid #e5e7eb;
        }

        .doodle-canvas {
            width: 100%;
            height: auto;
            display: block;
        }

        /* Hand cursor animation */
        .drawing-hand {
            position: absolute;
            width: 60px;
            height: 60px;
            pointer-events: none;
            z-index: 10;
            filter: drop-shadow(2px 4px 6px rgba(0,0,0,0.2));
            transition: all 0.1s ease;
        }

        .hand-svg {
            width: 100%;
            height: 100%;
            fill: #f4d03f;
            stroke: #2c3e50;
            stroke-width: 2;
        }

        /* Paper texture overlay */
        .paper-texture {
            position: absolute;
            inset: 0;
            opacity: 0.4;
            background-image: url("data:image/svg+xml,%3Csvg width='100' height='100' viewBox='0 0 100 100' xmlns='http://www.w3.org/2000/svg'%3E%3Cfilter id='noise'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.8' numOctaves='4' stitchTiles='stitch'/%3E%3C/filter%3E%3Crect width='100' height='100' filter='url(%23noise)' opacity='0.15'/%3E%3C/svg%3E");
            pointer-events: none;
        }

        /* Sketchy border effect */
        .sketchy-border {
            border: 3px solid #2c3e50;
            border-radius: 255px 15px 225px 15px / 15px 225px 15px 255px;
            position: relative;
        }

        /* Story section styling */
        .story-section {
            opacity: 0;
            transform: translateY(30px);
            transition: all 0.8s cubic-bezier(0.34, 1.56, 0.64, 1);
        }
        .story-section.visible {
            opacity: 1;
            transform: translateY(0);
        }

        /* Pencil scratch animation */
        @keyframes scratch {
            0%, 100% { transform: rotate(-5deg); }
            50% { transform: rotate(5deg); }
        }
        .scratching {
            animation: scratch 0.2s ease-in-out infinite;
        }

        /* Ink spread effect */
        .ink-spot {
            position: absolute;
            border-radius: 50%;
            background: radial-gradient(circle, rgba(0,0,0,0.1) 0%, transparent 70%);
            transform: scale(0);
            animation: inkSpread 0.6s ease-out forwards;
        }
        @keyframes inkSpread {
            to { transform: scale(3); opacity: 0; }
        }

        /* Color reveal animation */
        .color-reveal {
            filter: grayscale(100%) brightness(1.2);
            transition: filter 2s ease;
        }
        .color-reveal.colored {
            filter: grayscale(0%) brightness(1);
        }

        /* Progress indicators */
        .step-active { border-color: #7c3aed; background: #f3e8ff; }
        .step-complete { border-color: #10b981; background: #d1fae5; }
        
        .loading-pulse {
            animation: pulse 2s cubic-bezier(0.4, 0, 0.6, 1) infinite;
        }
        @keyframes pulse {
            0%, 100% { opacity: 1; }
            50% { opacity: .5; }
        }

        /* Scroll-triggered animations */
        .reveal-on-scroll {
            opacity: 0;
            transform: translateY(50px);
            transition: all 1s ease;
        }
        .reveal-on-scroll.revealed {
            opacity: 1;
            transform: translateY(0);
        }

        /* Watercolor bleed effect */
        .watercolor-bleed {
            position: relative;
        }
        .watercolor-bleed::before {
            content: '';
            position: absolute;
            inset: -10px;
            background: inherit;
            filter: blur(20px) saturate(1.5);
            opacity: 0.5;
            z-index: -1;
        }
    </style>
</head>
<body class="text-gray-800">

    <!-- API Configuration Modal -->
    <div id="api-config-modal" class="fixed inset-0 bg-black/50 z-50 flex items-center justify-center">
        <div class="glass-panel rounded-2xl p-8 max-w-md w-full mx-4">
            <h2 class="fairytale-font text-2xl font-bold mb-4">🔑 API Konfigurācija</h2>
            <div class="space-y-4">
                <div>
                    <label class="block text-sm font-semibold mb-1">Claude API Key</label>
                    <input type="password" id="claude-key" class="w-full px-3 py-2 rounded-lg border border-gray-300" placeholder="sk-ant-...">
                </div>
                <div>
                    <label class="block text-sm font-semibold mb-1">Gemini API Key</label>
                    <input type="password" id="gemini-key" class="w-full px-3 py-2 rounded-lg border border-gray-300" placeholder="AIza...">
                </div>
                <div>
                    <label class="block text-sm font-semibold mb-1">Banana.dev API Key (SDXL)</label>
                    <input type="password" id="banana-key" class="w-full px-3 py-2 rounded-lg border border-gray-300">
                </div>
                <button onclick="saveApiKeys()" class="w-full bg-purple-600 text-white py-2 rounded-lg font-semibold hover:bg-purple-700">
                    Saglabāt un Turpināt
                </button>
            </div>
        </div>
    </div>

    <!-- Navigation -->
    <nav class="glass-panel sticky top-0 z-40 border-b border-white/20">
        <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
            <div class="flex justify-between h-16 items-center">
                <div class="flex items-center space-x-3">
                    <span class="text-3xl">✏️</span>
                    <span class="fairytale-font text-2xl font-bold gradient-text">Pasaku Fabrika LIVE</span>
                </div>
                <div class="flex items-center space-x-4">
                    <div class="bg-purple-100 px-4 py-2 rounded-full text-purple-700 font-bold text-sm">
                        🎨 Doodle Video Mode
                    </div>
                </div>
            </div>
        </div>
    </nav>

    <main class="max-w-5xl mx-auto px-4 sm:px-6 lg:px-8 py-8">

        <!-- Generator Section -->
        <section id="generator" class="space-y-8">
            
            <!-- Input Panel -->
            <div class="glass-panel rounded-2xl p-6 shadow-xl mb-8">
                <h2 class="fairytale-font text-2xl font-bold mb-6 flex items-center">
                    <span class="mr-2">✨</span> Pasaku Parametri
                </h2>
                
                <div class="grid grid-cols-1 md:grid-cols-3 gap-4">
                    <div>
                        <label class="block text-sm font-semibold text-gray-700 mb-2">Bērna Vārds *</label>
                        <input type="text" id="child-name" placeholder="piem. Mairis" 
                            class="w-full px-4 py-3 rounded-lg border border-gray-300 focus:ring-2 focus:ring-purple-500">
                    </div>

                    <div>
                        <label class="block text-sm font-semibold text-gray-700 mb-2">Vecums</label>
                        <select id="child-age" class="w-full px-4 py-3 rounded-lg border border-gray-300">
                            <option value="3">3 gadi (6 attēli)</option>
                            <option value="4">4 gadi (7 attēli)</option>
                            <option value="5" selected>5 gadi (8 attēli)</option>
                            <option value="6">6 gadi (9 attēli)</option>
                            <option value="7">7 gadi (10 attēli)</option>
                        </select>
                    </div>

                    <div>
                        <label class="block text-sm font-semibold text-gray-700 mb-2">Zīmēšanas Stils</label>
                        <select id="doodle-style" class="w-full px-4 py-3 rounded-lg border border-gray-300">
                            <option value="crayon">Krītiņš uz papīra</option>
                            <option value="watercolor">Akvarelis</option>
                            <option value="pencil">Zīmulis</option>
                            <option value="marker">Marķieris</option>
                        </select>
                    </div>
                </div>

                <div class="mt-4 grid grid-cols-1 md:grid-cols-2 gap-4">
                    <div>
                        <label class="block text-sm font-semibold text-gray-700 mb-2">Tēma</label>
                        <select id="story-theme" class="w-full px-4 py-3 rounded-lg border border-gray-300">
                            <option value="dragon">🐉 Pūķis un dārgumi</option>
                            <option value="forest">🌲 Maģiskais mežs</option>
                            <option value="space">🚀 Kosmosa piedzīvojums</option>
                            <option value="ocean">🐠 Zemūdens pasaule</option>
                            <option value="princess">👑 Princese</option>
                        </select>
                    </div>
                    <div>
                        <label class="block text-sm font-semibold text-gray-700 mb-2">Mācību Mērķis</label>
                        <select id="learning-goal" class="w-full px-4 py-3 rounded-lg border border-gray-300">
                            <option value="">Tikai izklaide</option>
                            <option value="friendship">🤝 Draudzība</option>
                            <option value="courage">🦁 Drosme</option>
                            <option value="kindness">❤️ Laipnība</option>
                        </select>
                    </div>
                </div>

                <button onclick="startGeneration()" id="generate-btn"
                    class="mt-6 w-full bg-gradient-to-r from-purple-600 to-indigo-600 text-white py-4 rounded-xl font-bold text-lg hover:shadow-lg transform hover:scale-105 transition flex items-center justify-center space-x-2">
                    <span>✏️</span>
                    <span>Sākt Zīmēt Pasaku!</span>
                </button>
            </div>

            <!-- Generation Progress -->
            <div id="generation-progress" class="hidden glass-panel rounded-2xl p-6 shadow-xl">
                <h3 class="fairytale-font text-xl font-bold mb-4">🎨 Notiek Radīšana...</h3>
                <div class="space-y-3" id="progress-steps">
                    <!-- Steps injected here -->
                </div>
            </div>

            <!-- Live Story Viewer -->
            <div id="story-viewer" class="hidden">
                
                <!-- Title Section -->
                <div class="text-center mb-12 reveal-on-scroll">
                    <h1 id="story-title" class="fairytale-font text-4xl md:text-5xl font-bold text-gray-800 mb-4"></h1>
                    <p class="text-xl text-gray-600 handwritten">Priekš <span id="story-child" class="text-purple-600 font-bold"></span></p>
                </div>

                <!-- Dynamic Story Content -->
                <div id="story-content" class="space-y-16">
                    <!-- Sections injected here with doodles between -->
                </div>

                <!-- Controls -->
                <div class="fixed bottom-8 right-8 flex flex-col space-y-2">
                    <button onclick="scrollToNextDoodle()" class="bg-purple-600 text-white w-14 h-14 rounded-full shadow-lg hover:bg-purple-700 flex items-center justify-center text-2xl">
                        ⬇️
                    </button>
                    <button onclick="downloadStory()" class="bg-green-600 text-white w-14 h-14 rounded-full shadow-lg hover:bg-green-700 flex items-center justify-center text-2xl">
                        💾
                    </button>
                </div>

            </div>

            <!-- Empty State -->
            <div id="empty-state" class="glass-panel rounded-2xl p-12 shadow-xl text-center">
                <div class="text-6xl mb-4 animate-bounce">✏️</div>
                <h3 class="fairytale-font text-2xl font-bold text-gray-800 mb-2">Gatavs zīmēt?</h3>
                <p class="text-gray-600 mb-4">Katrs stāsts tiks ilustrēts ar dzīvajiem zīmējumiem, kas parādās acu priekšā!</p>
                <div class="flex justify-center space-x-4 text-sm text-gray-500">
                    <span>🤖 Claude AI</span>
                    <span>✏️ Doodle Animation</span>
                    <span>🎨 Gemini Images</span>
                </div>
            </div>

        </section>

    </main>

    <script>
        // Configuration
        let API_KEYS = {};
        let currentStory = null;
        let doodleObservers = [];

        // Load saved keys
        window.onload = () => {
            const saved = localStorage.getItem('api_keys');
            if (saved) {
                API_KEYS = JSON.parse(saved);
                document.getElementById('api-config-modal').classList.add('hidden');
            }
        };

        function saveApiKeys() {
            API_KEYS = {
                claude: document.getElementById('claude-key').value,
                gemini: document.getElementById('gemini-key').value,
                banana: document.getElementById('banana-key').value
            };
            localStorage.setItem('api_keys', JSON.stringify(API_KEYS));
            document.getElementById('api-config-modal').classList.add('hidden');
        }

        async function startGeneration() {
            const params = {
                name: document.getElementById('child-name').value || 'Mairis',
                age: parseInt(document.getElementById('child-age').value),
                theme: document.getElementById('story-theme').value,
                style: document.getElementById('doodle-style').value,
                learning: document.getElementById('learning-goal').value
            };

            // Show progress
            document.getElementById('empty-state').classList.add('hidden');
            document.getElementById('generation-progress').classList.remove('hidden');

            // Generate story structure
            const story = await generateStoryStructure(params);
            currentStory = story;

            // Generate images for each section
            await generateSectionImages(story);

            // Render story with doodle placeholders
            renderStory(story);

            // Hide progress
            document.getElementById('generation-progress').classList.add('hidden');
            document.getElementById('story-viewer').classList.remove('hidden');

            // Setup scroll observers for doodle animations
            setupDoodleAnimations();
        }

        async function generateStoryStructure(params) {
            // Simulate API call to Claude
            await simulateProgress('Claude ģenerē stāstu...', 2000);

            const numImages = params.age + 3; // 6-10 images based on age
            const sections = [];

            // Create story beats with image placement
            const beats = [
                { type: 'intro', imagePrompt: `Child ${params.name} looking out window at sunset, watercolor style, dreamy atmosphere` },
                { type: 'inciting', imagePrompt: `Magical fairy appearing in garden with sparkles, whimsical, ${params.style} style` },
                { type: 'rising1', imagePrompt: `Child and fairy walking through misty forest, adventure, storybook illustration` },
                { type: 'rising2', imagePrompt: `Crossing a silver river on a log, magical reflection, fantasy art` },
                { type: 'climax', imagePrompt: `Dark cave with glowing treasure, child being brave, dramatic lighting` },
                { type: 'falling', imagePrompt: `Discovery of friendship treasure, golden flowers, warm colors` },
                { type: 'resolution', imagePrompt: `Flying home on fairy wings, night sky, stars` },
                { type: 'ending', imagePrompt: `Child sleeping peacefully with crystal on windowsill, cozy bedroom` }
            ];

            // Adjust based on age
            const selectedBeats = beats.slice(0, numImages);

            const storyText = {
                title: `${params.name} un Maģiskā Dzirkstīte`,
                sections: selectedBeats.map((beat, idx) => ({
                    id: idx,
                    type: beat.type,
                    text: getSectionText(beat.type, params),
                    imagePrompt: beat.imagePrompt,
                    imageUrl: null, // Will be filled
                    audioMood: getMoodForType(beat.type)
                }))
            };

            return storyText;
        }

        function getSectionText(type, params) {
            const texts = {
                intro: `Katru vakaru, kad saule krāsoja debesis rozā un zelta toņos, mazais ${params.name} sēdēja pie loga un sapņoja par neparastiem piedzīvojumiem. "Šovakar notiks kas īpašs," domāja ${params.name}, jo vectēvs bija teicis, ka pilnmēness naktīs notiek brīnumi.`,
                
                inciting: `Pēkšņi dārzā iemirdzējās mazs, sārtas gaismiņas punkts. ${params.name} izskrēja ārā un ieraudzīja... pasaku būtni! Tā bija mazāka par peoniju, bet lielāka par zvirbuli, ar caurspīdīgiem spārniem, kas atspīdēja kā varavīksne. "Esmu Dzirkstīte," čukstēja būtne.`,
                
                rising1: `"Esmu atnākusi, lai aizvestu tevi uz vietu, kur mācās ${params.learning || 'draudzība'}," sacīja Dzirkstīte. "Vai tu drosmīgs, ${params.name}?" Ceļš sākās caur miglāju, kur koki čukstēja noslēpumus un zari žāvās kā veci draugi.`,
                
                rising2: `Tie nonāca pie upes, kur ūdens šķita no šķidrā sudraba. "Jābūt uzmanīgam," sacīja Dzirkstīte. "${params.name}, tu vari to izdarīt!" Un ${params.name} uzrāpās uz krituša koka, kas šķērsoja upi, soli pa solim, neatskatoties lejup.`,
                
                climax: `Tumsā aiz lielas akmeņa parādījās ēna. ${params.name} sirds sāka pukstēt ātrāk. Bet tad atskanēja čuksti: "Kas tur?" Izrādījās, ka tumšajā alā slēpjas ne briesmonis, bet... pazudušie pasaku grāmatu varoņi, kas gaidīja draugu!`,
                
                falling: `Alā viņi atrada dārgumu - ne zeltu, ne dārgakmeņus, bet grāmatu ar tukšām lapām. "Šeit tu rakstīsi savus piedzīvojumus," sacīja Dzirkstīte. ${params.name} saprata, ka īstais dārgums ir atmiņas, ko viņš radīja.`,
                
                resolution: `"Jāiet mājup," sacīja Dzirkstīte, un viņi aizlidoja virs mežiem, kur koku galotnes šķita kā mīksti zaļi mākoņi. ${params.name} juta, kā vējš glāsta matus, un zvaigznes šķita tik tuvu, ka varētu aizsniegt.`,
                
                ending: `Nākamajā rītā ${params.name} pamodās savā gultā. Vai tas bija tikai sapnis? Bet uz palodzes mirdzēja mazs kristāls - un uz grāmatzīmes bija rakstīts: "Brīnumi notiek katru dienu. Atceries to, ${params.name}."`
            };
            return texts[type] || texts.intro;
        }

        function getMoodForType(type) {
            const moods = {
                intro: 'calm',
                inciting: 'magical',
                rising1: 'adventure',
                rising2: 'tension',
                climax: 'dramatic',
                falling: 'warm',
                resolution: 'peaceful',
                ending: 'nostalgic'
            };
            return moods[type] || 'neutral';
        }

        async function generateSectionImages(story) {
            const progressContainer = document.getElementById('progress-steps');
            
            for (let i = 0; i < story.sections.length; i++) {
                const section = story.sections[i];
                
                // Create progress item
                const stepDiv = document.createElement('div');
                stepDiv.className = 'flex items-center space-x-3 p-3 rounded-lg bg-gray-50';
                stepDiv.innerHTML = `
                    <div class="w-8 h-8 rounded-full bg-purple-100 flex items-center justify-center text-purple-600">🎨</div>
                    <div class="flex-1">
                        <div class="font-semibold">Attēls ${i + 1}: ${section.type}</div>
                        <div class="text-sm text-gray-500 truncate">${section.imagePrompt}</div>
                    </div>
                    <span class="status text-sm font-semibold text-gray-400">Gaida...</span>
                `;
                progressContainer.appendChild(stepDiv);

                // Simulate image generation (in real app: call Banana.dev or Gemini)
                await new Promise(r => setTimeout(r, 1500));
                
                // Generate placeholder image with sketch effect
                section.imageUrl = `https://picsum.photos/800/600?random=${Date.now() + i}`;
                section.sketchUrl = createSketchVersion(section.imageUrl);
                
                stepDiv.querySelector('.status').textContent = '✅ Gatavs';
                stepDiv.classList.add('bg-green-50');
            }
        }

        function createSketchVersion(colorUrl) {
            // In real implementation, this would process through Canvas API
            // to create pencil sketch version for animation
            return colorUrl + '&grayscale';
        }

        function renderStory(story) {
            document.getElementById('story-title').textContent = story.title;
            document.getElementById('story-child').textContent = story.sections[0].text.match(/[A-Z][a-z]+/)?.[0] || 'Bērns';

            const container = document.getElementById('story-content');
            container.innerHTML = '';

            story.sections.forEach((section, idx) => {
                // Text section
                const textDiv = document.createElement('div');
                textDiv.className = 'story-section max-w-2xl mx-auto px-4';
                textDiv.innerHTML = `
                    <p class="text-xl md:text-2xl leading-relaxed text-gray-700 handwritten text-center">
                        ${section.text}
                    </p>
                `;
                container.appendChild(textDiv);

                // Doodle container (appears after text)
                const doodleDiv = document.createElement('div');
                doodleDiv.className = 'doodle-wrapper reveal-on-scroll my-12';
                doodleDiv.dataset.section = idx;
                doodleDiv.innerHTML = `
                    <div class="doodle-container sketchy-border" id="doodle-${idx}">
                        <div class="paper-texture"></div>
                        <canvas class="doodle-canvas" id="canvas-${idx}" width="800" height="600"></canvas>
                        
                        <!-- Drawing hand -->
                        <div class="drawing-hand" id="hand-${idx}">
                            <svg class="hand-svg" viewBox="0 0 100 100">
                                <!-- Simple hand holding pencil -->
                                <ellipse cx="50" cy="60" rx="25" ry="30" fill="#f4d03f" stroke="#2c3e50" stroke-width="2"/>
                                        <rect x="45" y="20" width="10" height="40" fill="#e74c3c" transform="rotate(-15 50 40)"/>
                                        <polygon points="40,20 60,20 55,5 45,5" fill="#f39c12" transform="rotate(-15 50 20)"/>
                                        <circle cx="35" cy="55" r="8" fill="#f4d03f" stroke="#2c3e50"/>
                                        <circle cx="65" cy="55" r="8" fill="#f4d03f" stroke="#2c3e50"/>
                                        <circle cx="50" cy="75" r="8" fill="#f4d03f" stroke="#2c3e50"/>
                            </svg>
                        </div>
                        
                        <!-- Caption -->
                        <div class="absolute bottom-4 left-4 right-4 text-center">
                            <span class="handwritten text-gray-600 text-lg bg-white/80 px-4 py-1 rounded-full">
                                Zīmējam: ${section.type}...
                            </span>
                        </div>
                    </div>
                    
                    <!-- Audio indicator -->
                    <div class="flex justify-center mt-4 space-x-2">
                        <span class="text-sm text-gray-500 bg-white/50 px-3 py-1 rounded-full">
                            🎵 ${section.audioMood}
                        </span>
                    </div>
                `;
                container.appendChild(doodleDiv);
            });

            // Reveal title immediately
            setTimeout(() => {
                document.querySelector('.reveal-on-scroll').classList.add('revealed');
            }, 100);
        }

        function setupDoodleAnimations() {
            // Clear previous observers
            doodleObservers.forEach(obs => obs.disconnect());
            doodleObservers = [];

            const observerOptions = {
                root: null,
                rootMargin: '0px',
                threshold: 0.3
            };

            const observer = new IntersectionObserver((entries) => {
                entries.forEach(entry => {
                    if (entry.isIntersecting && !entry.target.classList.contains('animated')) {
                        entry.target.classList.add('revealed');
                        entry.target.classList.add('animated');
                        
                        const sectionIdx = entry.target.dataset.section;
                        if (sectionIdx !== undefined) {
                            setTimeout(() => {
                                animateDoodle(parseInt(sectionIdx));
                            }, 500);
                        }
                    }
                });
            }, observerOptions);

            // Observe all story sections and doodle wrappers
            document.querySelectorAll('.story-section, .doodle-wrapper').forEach(el => {
                observer.observe(el);
            });

            doodleObservers.push(observer);
        }

        async function animateDoodle(sectionIdx) {
            const section = currentStory.sections[sectionIdx];
            const canvas = document.getElementById(`canvas-${sectionIdx}`);
            const ctx = canvas.getContext('2d');
            const hand = document.getElementById(`hand-${sectionIdx}`);
            
            // Set canvas size
            canvas.width = 800;
            canvas.height = 600;
            
            // Load image
            const img = new Image();
            img.crossOrigin = "anonymous";
            img.src = section.imageUrl;
            
            await new Promise(resolve => {
                img.onload = resolve;
            });

            // Animation parameters
            const duration = 4000; // 4 seconds to "draw"
            const startTime = Date.now();
            
            // Create sketch path (simplified as random scribbles for demo)
            const paths = generateSketchPaths(canvas.width, canvas.height, 20);
            
            // Animation loop
            function animate() {
                const elapsed = Date.now() - startTime;
                const progress = Math.min(elapsed / duration, 1);
                
                // Clear canvas
                ctx.fillStyle = '#fffef7';
                ctx.fillRect(0, 0, canvas.width, canvas.height);
                
                // Draw paper texture effect
                ctx.fillStyle = 'rgba(0,0,0,0.02)';
                for (let i = 0; i < 1000; i++) {
                    ctx.fillRect(Math.random() * canvas.width, Math.random() * canvas.height, 2, 2);
                }
                
                // Draw sketch lines up to current progress
                ctx.strokeStyle = '#2c3e50';
                ctx.lineWidth = 2;
                ctx.lineCap = 'round';
                ctx.lineJoin = 'round';
                
                const pathsToDraw = Math.floor(paths.length * progress);
                
                for (let i = 0; i < pathsToDraw; i++) {
                    const path = paths[i];
                    ctx.beginPath();
                    ctx.moveTo(path[0].x, path[0].y);
                    
                    const pathProgress = (i === pathsToDraw - 1) ? 
                        ((paths.length * progress) - pathsToDraw) * path.length : 
                        path.length;
                    
                    for (let j = 1; j < Math.min(path.length, Math.floor(pathProgress) + 1); j++) {
                        ctx.lineTo(path[j].x, path[j].y);
                    }
                    ctx.stroke();
                }
                
                // Update hand position to end of current line
                if (pathsToDraw > 0 && pathsToDraw <= paths.length) {
                    const currentPath = paths[pathsToDraw - 1];
                    const pointIdx = Math.min(
                        Math.floor(((paths.length * progress) - pathsToDraw + 1) * currentPath.length),
                        currentPath.length - 1
                    );
                    const point = currentPath[Math.max(0, pointIdx)];
                    
                    hand.style.left = (point.x / canvas.width * 100) + '%';
                    hand.style.top = (point.y / canvas.height * 100) + '%';
                    
                    // Add scratching effect near end
                    if (progress > 0.8) {
                        hand.classList.add('scratching');
                    }
                }
                
                if (progress < 1) {
                    requestAnimationFrame(animate);
                } else {
                    // Reveal full color image
                    finishDoodle(canvas, ctx, img, hand);
                }
            }
            
            animate();
        }

        function generateSketchPaths(width, height, count) {
            const paths = [];
            for (let i = 0; i < count; i++) {
                const path = [];
                let x = Math.random() * width;
                let y = Math.random() * height;
                
                for (let j = 0; j < 20; j++) {
                    path.push({ x, y });
                    x += (Math.random() - 0.5) * 100;
                    y += (Math.random() - 0.5) * 100;
                }
                paths.push(path);
            }
            return paths;
        }

        function finishDoodle(canvas, ctx, img, hand) {
            // Fade in color image over sketch
            hand.style.opacity = '0';
            hand.classList.remove('scratching');
            
            let opacity = 0;
            function fadeIn() {
                opacity += 0.02;
                ctx.globalAlpha = 1;
                ctx.fillStyle = '#fffef7';
                ctx.fillRect(0, 0, canvas.width, canvas.height);
                
                // Redraw sketch lightly
                ctx.globalAlpha = 0.3;
                ctx.strokeStyle = '#2c3e50';
                ctx.lineWidth = 1;
                for (let i = 0; i < 50; i++) {
                    ctx.beginPath();
                    ctx.moveTo(Math.random() * canvas.width, Math.random() * canvas.height);
                    ctx.lineTo(Math.random() * canvas.width, Math.random() * canvas.height);
                    ctx.stroke();
                }
                
                // Draw color image
                ctx.globalAlpha = opacity;
                ctx.drawImage(img, 0, 0, canvas.width, canvas.height);
                
                if (opacity < 1) {
                    requestAnimationFrame(fadeIn);
                } else {
                    // Add watercolor bleed effect
                    addWatercolorEffect(canvas, ctx);
                }
            }
            fadeIn();
        }

        function addWatercolorEffect(canvas, ctx) {
            // Simulate watercolor bleeding at edges
            const imageData = ctx.getImageData(0, 0, canvas.width, canvas.height);
            const data = imageData.data;
            
            for (let i = 0; i < data.length; i += 4) {
                if (Math.random() > 0.99) {
                    const bleed = Math.random() * 20;
                    data[i] = Math.min(255, data[i] + bleed);     // R
                    data[i+1] = Math.min(255, data[i+1] + bleed); // G
                    data[i+2] = Math.min(255, data[i+2] + bleed); // B
                }
            }
            
            ctx.putImageData(imageData, 0, 0);
        }

        function scrollToNextDoodle() {
            const doodles = document.querySelectorAll('.doodle-wrapper:not(.revealed)');
            if (doodles.length > 0) {
                doodles[0].scrollIntoView({ behavior: 'smooth', block: 'center' });
            }
        }

        function downloadStory() {
            // Create printable version
            const printWindow = window.open('', '_blank');
            printWindow.document.write(`
                <html>
                <head>
                    <title>${currentStory.title}</title>
                    <style>
                        body { font-family: Georgia, serif; max-width: 800px; margin: 0 auto; padding: 40px; }
                        h1 { text-align: center; color: #4c1d95; }
                        .section { margin: 40px 0; page-break-inside: avoid; }
                        .text { font-size: 18px; line-height: 1.8; margin-bottom: 20px; }
                        .image { text-align: center; margin: 30px 0; }
                        .image img { max-width: 100%; border-radius: 10px; box-shadow: 0 4px 6px rgba(0,0,0,0.1); }
                    </style>
                </head>
                <body>
                    <h1>${currentStory.title}</h1>
                    ${currentStory.sections.map(s => `
                        <div class="section">
                            <div class="text">${s.text}</div>
                            <div class="image">
                                <img src="${s.imageUrl}" alt="Illustration">
                            </div>
                        </div>
                    `).join('')}
                </body>
                </html>
            `);
            printWindow.document.close();
            printWindow.print();
        }

        async function simulateProgress(text, duration) {
            return new Promise(resolve => setTimeout(resolve, duration));
        }
    </script>
</body>
</html>
