import os
from flask import Flask, render_template_string, send_from_directory

app = Flask(__name__)

# Route សម្រាប់ទាញយក File រូបភាព Logo ផ្ទាល់ពី folder images/
@app.route('/images/<path:filename>')
def serve_images(filename):
    return send_from_directory(os.path.join(app.root_path, 'images'), filename)

HTML_CODE = """
<!DOCTYPE html>
<html lang="km">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>បញ្ជីវត្តមានសិស្ស - Tongpor Special Part-Time School</title>
    <!-- Tailwind CSS -->
    <script src="https://cdn.tailwindcss.com"></script>
    <!-- Google Khmer Fonts -->
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Battambang:wght@400;700&family=Moul&family=Siemreap&display=swap" rel="stylesheet">
    <!-- html2canvas សម្រាប់ Export ជារូបភាព PNG -->
    <script src="https://cdnjs.cloudflare.com/ajax/libs/html2canvas/1.4.1/html2canvas.min.js"></script>

    <style>
        body {
            font-family: 'Battambang', sans-serif;
            background-color: #111827;
            margin: 0;
            padding: 0;
            -webkit-print-color-adjust: exact !important;
            print-color-adjust: exact !important;
        }
        .font-moul { font-family: 'Moul', cursive; }
        .font-siemreap { font-family: 'Siemreap', sans-serif; }
        
        /* ម៉ូដអក្សរព័ត៌មានគ្រូ និង ប្រចាំខែ (Siemreap, 16px, ពណ៌ខ្មៅ) */
        .teacher-info-custom {
            font-family: 'Siemreap', sans-serif !important;
            font-size: 16px !important;
            color: #000000 !important; /* ពណ៌ខ្មៅ */
            font-weight: normal !important;
        }

        /* ប្រអប់វាយអក្សរឈ្មោះគ្រូ និងភេទ៖ លើកអក្សរឡើងលើ មិនឱ្យជើងអក្សរជាន់បន្ទាត់ដាច់ខាត */
        .field-teacher-line {
            outline: none;
            cursor: text;
            display: inline-block;
            border-bottom: 1px dotted #000000 !important;
            padding-bottom: 5px !important; /* ផ្តល់គម្លាតកុំឱ្យជើងអក្សរជាន់បន្ទាត់ */
            line-height: 1.2 !important;
            background: transparent;
        }
        .field-teacher-line:focus {
            background-color: #eff6ff !important;
            border-bottom: 1.5px solid #2563eb !important;
        }

        /* បន្ទាត់ប្រចាំខែ */
        .month-line {
            border-bottom: 1px dotted #000000 !important;
            padding-bottom: 5px !important; /* ផ្តល់គម្លាតកុំឱ្យជើងអក្សរ វិច្ឆិកា ជាន់បន្ទាត់ */
            line-height: 1.2 !important;
            display: inline-block;
        }
        
        /* សន្លឹក A4 Landscape */
        .page-landscape {
            width: 297mm;
            min-height: 210mm;
            margin: 15px auto;
            background: #ffffff;
            padding: 8mm 10mm;
            box-shadow: 0 4px 25px rgba(0, 0, 0, 0.6);
            box-sizing: border-box;
            position: relative;
        }
        .bg-yellow-header { background-color: #fff200 !important; }
        
        /* Table Layout ចាក់សោរ Column និងកម្រាស់បន្ទាត់ច្បាស់ */
        .attendance-table {
            border: 1.5px solid black !important;
            border-collapse: collapse !important;
            table-layout: fixed !important;
            width: 100% !important;
        }
        .attendance-table th, .attendance-table td {
            border: 1px solid black !important;
            box-sizing: border-box !important;
            text-align: center !important;
            vertical-align: middle !important;
            padding: 0 !important;
            margin: 0 !important;
        }

        /* កម្ពស់ក្រឡាជួរដេក 34px ធានាអក្សរទំហំ 16px នៅចំកណ្តាល និងមិនជាន់បន្ទាត់ */
        .attendance-table tbody tr {
            height: 34px !important;
        }

        .day-header-top {
            height: 20px;
            line-height: 20px;
            font-size: 8.5px;
            font-weight: 600;
            border-bottom: 1px solid black;
        }
        .day-header-bottom {
            height: 20px;
            line-height: 20px;
            font-size: 9px;
            font-weight: bold;
        }

        /* ឈ្មោះសិស្ស Font Siemreap Size 16 មិនដិត នៅចំកណ្តាលក្រឡាស្មើលើក្រោមឆ្វេងស្តាំ */
        .student-name-cell {
            font-size: 16px !important;
            font-family: 'Siemreap', sans-serif !important;
            font-weight: normal !important;
            text-align: center !important;
            vertical-align: middle !important;
            line-height: normal !important;
            height: 34px !important;
            padding: 2px 6px !important;
            border-bottom: 1px solid black !important;
            white-space: nowrap !important;
            overflow: hidden !important;
            text-overflow: ellipsis !important;
        }

        /* លេខរៀងសិស្ស នៅចំកណ្តាល */
        .no-cell {
            font-size: 12px !important;
            font-weight: bold !important;
            font-family: Arial, sans-serif !important;
            text-align: center !important;
            vertical-align: middle !important;
            line-height: normal !important;
            height: 34px !important;
        }

        /* ប្រអប់វាយអក្សរទូទៅ */
        .field-editable {
            outline: none;
            cursor: text;
            display: inline-block;
            border-bottom: 1px dotted black;
            min-height: 20px;
            line-height: 20px;
            background: transparent;
        }
        .field-editable:focus {
            background-color: #eff6ff !important;
            border-bottom: 1.5px solid #2563eb !important;
        }

        /* និមិត្តសញ្ញាវត្តមាន */
        .status-P { color: #000000 !important; font-weight: 900; font-size: 14px; }
        .status-L { color: #2563eb !important; font-weight: 800; font-size: 12px; }
        .status-A { color: #dc2626 !important; font-weight: 800; font-size: 12px; }
        
        .day-cell {
            cursor: pointer;
            user-select: none;
            height: 34px !important;
            line-height: normal !important;
            font-family: Arial, sans-serif !important;
            text-align: center !important;
            vertical-align: middle !important;
            border-bottom: 1px solid black !important;
            transition: background 0.1s;
            padding: 0 !important;
        }
        .day-cell:hover {
            background-color: #fef08a !important;
        }

        .btn-mode-active {
            outline: 2px solid #ffffff;
            transform: scale(1.05);
            box-shadow: 0 0 10px rgba(255, 255, 255, 0.7);
        }

        /* Modal សម្រាប់ Save រូបភាពលើទូរស័ព្ទ */
        #mobile-save-modal {
            display: none;
            position: fixed;
            inset: 0;
            background: rgba(0, 0, 0, 0.85);
            z-index: 9999;
            align-items: center;
            justify-content: center;
            padding: 15px;
        }

        @media print {
            body { background: white !important; }
            .no-print { display: none !important; }
            .page-landscape {
                margin: 0 !important;
                padding: 4mm 6mm !important;
                box-shadow: none !important;
                width: 100% !important;
            }
            @page { size: A4 landscape; margin: 2mm; }
        }
    </style>
</head>
<body class="text-black">

    <!-- របារ Toolbar -->
    <div class="no-print bg-slate-900 text-white p-2.5 shadow-xl sticky top-0 z-50 flex flex-wrap items-center justify-between px-6 border-b border-slate-700">
        <div class="flex items-center space-x-3">
            <span class="font-bold text-sm text-amber-400">📋 ប្រព័ន្ធវត្តមានសិស្ស</span>
            
            <div class="flex items-center space-x-1.5 bg-slate-800 px-2 py-1 rounded border border-slate-600 text-xs">
                <span>ខែ៖</span>
                <select id="select-month" onchange="changeCalendar()" class="bg-slate-700 text-white rounded px-1.5 py-0.5 outline-none font-bold">
                    <option value="0">មករា</option>
                    <option value="1">កុម្ភៈ</option>
                    <option value="2">មីនា</option>
                    <option value="3">មេសា</option>
                    <option value="4">ឧសភា</option>
                    <option value="5">មិថុនា</option>
                    <option value="6">កក្កដា</option>
                    <option value="7">សីហា</option>
                    <option value="8">កញ្ញា</option>
                    <option value="9">តុលា</option>
                    <option value="10">វិច្ឆិកា</option>
                    <option value="11">ធ្នូ</option>
                </select>
                <select id="select-year" onchange="changeCalendar()" class="bg-slate-700 text-white rounded px-1.5 py-0.5 outline-none font-bold"></select>
            </div>

            <!-- សញ្ញាវត្តមាន -->
            <div class="flex items-center space-x-1 bg-slate-800 p-1 rounded-lg border border-slate-700">
                <span class="text-[11px] text-gray-300 mr-1 ml-1 font-semibold">ជ្រើសសញ្ញា៖</span>
                <button type="button" onclick="setMode('P', this)" id="btn-mode-P" class="bg-zinc-800 hover:bg-black text-white text-xs font-bold px-2.5 py-1 rounded border border-gray-500 shadow flex items-center">
                    <span class="text-white font-extrabold mr-1">✓</span> មក
                </button>
                <button type="button" onclick="setMode('L', this)" id="btn-mode-L" class="bg-blue-600 hover:bg-blue-500 text-white text-xs font-bold px-2.5 py-1 rounded shadow flex items-center">
                    🔵 ច្បាប់ (P)
                </button>
                <button type="button" onclick="setMode('A', this)" id="btn-mode-A" class="bg-red-600 hover:bg-red-500 text-white text-xs font-bold px-2.5 py-1 rounded shadow flex items-center">
                    🔴 ឈប់ (A)
                </button>
                <button type="button" onclick="setMode('CLEAR', this)" id="btn-mode-CLEAR" class="bg-gray-600 hover:bg-gray-500 text-white text-xs font-bold px-2 py-1 rounded shadow">
                    🧹 លុប
                </button>
                <button type="button" onclick="setMode('AUTO', this)" id="btn-mode-AUTO" class="bg-slate-700 hover:bg-slate-600 text-amber-300 text-xs font-bold px-2 py-1 rounded shadow btn-mode-active">
                    🔄 វិលជុំ
                </button>
            </div>
        </div>

        <div class="flex items-center space-x-2">
            <button onclick="addNewRow()" class="bg-indigo-600 hover:bg-indigo-700 text-white px-2.5 py-1.5 rounded text-xs font-bold shadow">➕ ថែមសិស្ស</button>
            <button onclick="saveData(true)" class="bg-emerald-600 hover:bg-emerald-700 text-white px-2.5 py-1.5 rounded text-xs font-bold shadow">💾 រក្សាទុក</button>
            <button onclick="exportAsImage()" id="btn-export-img" class="bg-purple-600 hover:bg-purple-700 text-white px-3 py-1.5 rounded text-xs font-bold shadow flex items-center">
                📱/🖼️ Save ជារូបភាព
            </button>
            <button onclick="window.print()" class="bg-rose-600 hover:bg-rose-700 text-white px-3 py-1.5 rounded text-xs font-bold shadow">📄 Export ជា PDF</button>
            <button onclick="resetData()" class="bg-amber-600 hover:bg-amber-700 text-white px-2 py-1.5 rounded text-xs font-bold shadow">🔄 Reset</button>
        </div>
    </div>

    <!-- សន្លឹកទម្រង់ A4 Landscape -->
    <div class="page-landscape" id="capture-area">

        <!-- ក្បាលទំព័រ Header -->
        <div class="flex justify-between items-start mb-2">
            <!-- ឆ្វេង: រូបភាព Logo សាលា (អាចចុចលើរូបដើម្បីប្តូរ ឬ Upload ផ្ទាល់បាន) -->
            <div class="flex items-center space-x-2.5 w-[34%]">
                <div class="w-[75px] h-[75px] min-w-[75px] min-h-[75px] flex items-center justify-center flex-shrink-0 relative group cursor-pointer" onclick="document.getElementById('logo-file-input').click()" title="ចុចទីនេះដើម្បីប្តូររូបភាព Logo">
                    <img src="/images/logo.png" id="school-logo" class="w-full h-full object-contain aspect-square" alt="Logo" onerror="this.onerror=null; this.src='https://ui-avatars.com/api/?name=TPPS&background=0284c7&color=fff&size=128&rounded=true';" />
                    <input type="file" id="logo-file-input" accept="image/*" class="hidden" onchange="handleLogoUpload(event)">
                    <div class="no-print absolute inset-0 bg-black/50 text-white text-[9px] rounded-full flex flex-col items-center justify-center opacity-0 group-hover:opacity-100 transition-opacity">
                        <span>📷 ប្តូរ Logo</span>
                    </div>
                </div>
                <div>
                    <h1 class="font-moul text-[13px] tracking-wide leading-snug">សាលាបង្រៀនគួរពិសេស តុងប៉</h1>
                    <h2 class="text-[11px] font-bold tracking-tight font-sans">Tong Po Special Part Time School</h2>
                </div>
            </div>

            <!-- កណ្តាល: ប្រអប់ពងក្រពើ (Pills) -->
            <div class="flex flex-col items-center w-[33%] pt-0.5">
                <div class="border-[1.5px] border-black rounded-full px-3 py-0.5 flex items-center w-full justify-center text-xs">
                    <span class="font-moul mr-1.5 text-[10px] whitespace-nowrap">បញ្ជីវត្តមានសិស្សថ្នាក់</span>
                    <span contenteditable="true" id="class_name" class="field-editable flex-1 text-center px-1 text-xs min-w-[120px]"></span>
                </div>
                <div class="flex space-x-2 mt-1.5 w-full">
                    <div class="border-[1.5px] border-black rounded-full px-3 py-0.5 flex items-center w-1/2 text-xs">
                        <span class="font-bold mr-1.5 whitespace-nowrap">អគារ</span>
                        <span contenteditable="true" id="building_name" class="field-editable w-full text-center text-xs"></span>
                    </div>
                    <div class="border-[1.5px] border-black rounded-full px-3 py-0.5 flex items-center w-1/2 text-xs">
                        <span class="font-bold mr-1.5 whitespace-nowrap">បន្ទប់</span>
                        <span contenteditable="true" id="room_name" class="field-editable w-full text-center text-xs"></span>
                    </div>
                </div>
            </div>

            <!-- ស្តាំ: ព្រះរាជាណាចក្រកម្ពុជា -->
            <div class="text-center w-[33%] flex flex-col items-end">
                <div class="text-center w-[230px]">
                    <h1 class="font-moul text-xs leading-relaxed">ព្រះរាជាណាចក្រកម្ពុជា</h1>
                    <h2 class="font-moul text-xs leading-relaxed">ជាតិ សាសនា ព្រះមហាក្សត្រ</h2>
                    <div class="flex justify-center items-center my-0.5">
                        <svg width="120" height="15" viewBox="0 0 160 20">
                            <path d="M 10 12 C 16 6 22 14 28 10 C 25 14 18 16 10 12 Z" fill="#222"/>
                            <path d="M 30 12 C 36 6 42 14 48 10 C 45 14 38 16 30 12 Z" fill="#222"/>
                            <g fill="#D32F2F" stroke="#D32F2F" stroke-width="0.5">
                                <circle cx="64" cy="10" r="1.5"/>
                                <path d="M 64 4 L 64 16 M 58 10 L 70 10 M 60 6 L 68 14 M 60 14 L 68 6"/>
                                <circle cx="80" cy="10" r="1.5"/>
                                <path d="M 80 4 L 80 16 M 74 10 L 86 10 M 76 6 L 84 14 M 76 14 L 84 6"/>
                                <circle cx="96" cy="10" r="1.5"/>
                                <path d="M 96 4 L 96 16 M 90 10 L 102 10 M 92 6 L 100 14 M 92 14 L 100 6"/>
                            </g>
                            <path d="M 112 10 C 118 14 124 6 130 12 C 122 16 115 14 112 10 Z" fill="#222"/>
                            <path d="M 132 10 C 138 14 144 6 150 12 C 142 16 135 14 132 10 Z" fill="#222"/>
                        </svg>
                    </div>
                </div>
            </div>
        </div>

        <!-- ព័ត៌មានគ្រូ & កាលបរិច្ឆេទ (Font Siemreap 16px ពណ៌ខ្មៅសុទ្ធ មិនជាន់បន្ទាត់) -->
        <div class="flex justify-between items-end text-xs mb-3 font-sans">
            <div class="w-[45%] space-y-2">
                <div class="flex items-baseline">
                    <span class="teacher-info-custom whitespace-nowrap font-bold">Name of Teacher:</span>
                    <span contenteditable="true" id="teacher_name" class="field-teacher-line teacher-info-custom flex-1 ml-2 px-1 text-left"></span>
                </div>
                <div class="flex items-baseline">
                    <span class="teacher-info-custom whitespace-nowrap font-bold">Sex:</span>
                    <span contenteditable="true" id="teacher_sex" class="field-teacher-line teacher-info-custom flex-1 ml-2 px-1 text-left"></span>
                </div>
            </div>
            <div class="w-[53%] space-y-2">
                <div class="flex items-baseline justify-end">
                    <span class="teacher-info-custom whitespace-nowrap font-bold mr-1">ប្រចាំខែ៖</span>
                    <span id="khmer_month_label" class="teacher-info-custom month-line min-w-[105px] text-center px-1"></span>
                    <span class="font-bold ml-2 text-xs">Date:</span>
                    <span contenteditable="true" id="doc_date" class="field-editable w-24 mx-1 text-center text-xs"></span>
                    <span class="font-bold ml-1 text-xs">Time:</span>
                    <span contenteditable="true" id="doc_time" class="field-editable w-20 ml-1 text-center text-xs"></span>
                </div>
                <div class="flex items-baseline justify-end">
                    <span class="font-bold whitespace-nowrap text-xs">phonenumber:</span>
                    <span contenteditable="true" id="phone_number" class="field-editable w-64 ml-1 px-1 text-left text-xs"></span>
                </div>
            </div>
        </div>

        <!-- តារាងវត្តមានសិស្ស ចាក់សោរ Colgroup និងទទឹងក្រឡា 100% -->
        <table class="attendance-table text-[10px]" id="main-table">
            <colgroup id="table-colgroup">
                <col style="width: 32px;">
                <col style="width: 160px;">
                <col style="width: 34px;">
                <!-- Col សម្រាប់ថ្ងៃនីមួយៗបញ្ចូលតាម JS -->
                <col id="col-phone-s" style="width: 95px;">
                <col id="col-phone-p" style="width: 95px;">
                <col id="col-del" style="width: 25px;">
            </colgroup>
            <thead>
                <tr class="bg-yellow-header font-bold text-[10px] h-[40px]" id="header-row">
                    <th style="height: 40px;">Nº</th>
                    <th style="height: 40px;">Name</th>
                    <th style="height: 40px;">Sex</th>
                    <!-- ថ្ងៃត្រូវបានបង្កើតតាម JavaScript -->
                    <th id="th-phone-student" style="height: 40px;">Phone Student</th>
                    <th id="th-phone-parent" style="height: 40px;">Phone Parent</th>
                    <th id="th-delete" style="height: 40px;" class="no-print bg-white border-0 text-red-400">លុប</th>
                </tr>
            </thead>
            <tbody id="student-rows"></tbody>
        </table>
    </div>

    <!-- Modal បង្ហាញរូបភាពសម្រាប់ទូរស័ព្ទដៃ -->
    <div id="mobile-save-modal" class="no-print flex flex-col">
        <div class="bg-white rounded-lg p-3 max-w-[95vw] max-h-[90vh] overflow-y-auto text-center shadow-2xl">
            <div class="flex justify-between items-center mb-2 pb-1 border-b">
                <span class="font-bold text-sm text-slate-800">📱 រក្សាទុករូបភាពលើទូរស័ព្ទ</span>
                <button onclick="closeMobileModal()" class="text-gray-500 hover:text-black font-bold text-lg px-2">✕</button>
            </div>
            <p class="text-xs text-rose-600 font-bold mb-2">👉 សូមចុចសង្កត់លើរូបភាព (Long-Press) រួចជ្រើសរើស "Save Image" ឬ "ទាញយករូបភាព"</p>
            <div class="border border-gray-300 rounded overflow-hidden mb-3">
                <img id="mobile-preview-img" src="" class="w-full h-auto object-contain" alt="Attendance Sheet Preview">
            </div>
            <div class="flex justify-center space-x-2">
                <a id="mobile-download-link" href="#" download="" class="bg-emerald-600 text-white text-xs font-bold px-4 py-2 rounded shadow">
                    📥 ចុចទាញយក (Download)
                </a>
                <button onclick="closeMobileModal()" class="bg-gray-600 text-white text-xs font-bold px-4 py-2 rounded shadow">
                    បិទ
                </button>
            </div>
        </div>
    </div>

    <!-- JavaScript -->
    <script>
        const khmerMonths = ["មករា", "កុម្ភៈ", "មីនា", "មេសា", "ឧសភា", "មិថុនា", "កក្កដា", "សីហា", "កញ្ញា", "តុលា", "វិច្ឆិកា", "ធ្នូ"];
        const dayNames = ["Su", "Mo", "Tu", "We", "Th", "Fr", "Sa"];
        
        let currentYear = new Date().getFullYear();
        let currentMonth = new Date().getMonth();
        let daysInMonth = 31;
        let selectedMode = 'AUTO';

        // មុខងារ Upload និងរក្សាទុក Logo ក្នុង Browser
        function handleLogoUpload(event) {
            const file = event.target.files[0];
            if (file) {
                const reader = new FileReader();
                reader.onload = function(e) {
                    const base64Data = e.target.result;
                    document.getElementById('school-logo').src = base64Data;
                    localStorage.setItem('school_logo_saved', base64Data);
                };
                reader.readAsDataURL(file);
            }
        }

        function loadSavedLogo() {
            const savedLogo = localStorage.getItem('school_logo_saved');
            if (savedLogo) {
                document.getElementById('school-logo').src = savedLogo;
            }
        }

        function setMode(mode, btn) {
            selectedMode = mode;
            document.querySelectorAll('#btn-mode-P, #btn-mode-L, #btn-mode-A, #btn-mode-CLEAR, #btn-mode-AUTO').forEach(b => {
                b.classList.remove('btn-mode-active');
            });
            btn.classList.add('btn-mode-active');
        }

        function initYearOptions() {
            const ySelect = document.getElementById('select-year');
            ySelect.innerHTML = '';
            for (let y = currentYear - 2; y <= currentYear + 3; y++) {
                const opt = document.createElement('option');
                opt.value = y;
                opt.innerText = y;
                if (y === currentYear) opt.selected = true;
                ySelect.appendChild(opt);
            }
            document.getElementById('select-month').value = currentMonth;
        }

        function changeCalendar() {
            currentMonth = parseInt(document.getElementById('select-month').value);
            currentYear = parseInt(document.getElementById('select-year').value);
            daysInMonth = new Date(currentYear, currentMonth + 1, 0).getDate();
            document.getElementById('khmer_month_label').innerText = khmerMonths[currentMonth] + " " + currentYear;
            buildTableHeaders();
            renderTable();
        }

        function buildTableHeaders() {
            const headerRow = document.getElementById('header-row');
            const refNode = document.getElementById('th-phone-student');
            
            const colGroup = document.getElementById('table-colgroup');
            const colRefNode = document.getElementById('col-phone-s');

            document.querySelectorAll('.day-header-col').forEach(el => el.remove());
            document.querySelectorAll('.day-col-tag').forEach(el => el.remove());

            for (let d = 1; d <= daysInMonth; d++) {
                const dateObj = new Date(currentYear, currentMonth, d);
                const dayStr = dayNames[dateObj.getDay()];

                const col = document.createElement('col');
                col.className = 'day-col-tag';
                col.style.width = '21px';
                colGroup.insertBefore(col, colRefNode);

                const th = document.createElement('th');
                th.className = 'day-header-col bg-yellow-header';
                th.style.height = '40px';
                th.innerHTML = `
                    <div class="day-header-top">${dayStr}</div>
                    <div class="day-header-bottom">${d}</div>
                `;
                headerRow.insertBefore(th, refNode);
            }
        }

        function handleCellClick(td) {
            if (selectedMode === 'P') {
                td.innerText = '✓';
                td.className = 'day-cell text-center status-P';
            } else if (selectedMode === 'L') {
                td.innerText = 'P';
                td.className = 'day-cell text-center status-L';
            } else if (selectedMode === 'A') {
                td.innerText = 'A';
                td.className = 'day-cell text-center status-A';
            } else if (selectedMode === 'CLEAR') {
                td.innerText = '';
                td.className = 'day-cell text-center';
            } else {
                const val = td.innerText.trim();
                if (val === '') {
                    td.innerText = '✓';
                    td.className = 'day-cell text-center status-P';
                } else if (val === '✓') {
                    td.innerText = 'P';
                    td.className = 'day-cell text-center status-L';
                } else if (val === 'P') {
                    td.innerText = 'A';
                    td.className = 'day-cell text-center status-A';
                } else {
                    td.innerText = '';
                    td.className = 'day-cell text-center';
                }
            }
            saveData(false);
        }

        // កម្ពស់ 34px និង Font Siemreap 16px មិនដិត
        function createRowHTML(index, data = {}) {
            let daysTd = '';
            for (let i = 1; i <= daysInMonth; i++) {
                let val = (data.days && data.days[i - 1]) ? data.days[i - 1] : '';
                let statusClass = '';
                if (val === '✓') statusClass = 'status-P';
                else if (val === 'P') statusClass = 'status-L';
                else if (val === 'A') statusClass = 'status-A';

                daysTd += `<td onclick="handleCellClick(this)" class="day-cell ${statusClass}">${val}</td>`;
            }
            return `
                <tr class="h-[34px]">
                    <td class="no-cell">${index}</td>
                    <td contenteditable="true" class="editable student-name-cell">${data.name || ''}</td>
                    <td contenteditable="true" class="editable text-center text-xs">${data.sex || ''}</td>
                    ${daysTd}
                    <td contenteditable="true" class="editable text-center font-mono text-[9.5px]">${data.phone_student || ''}</td>
                    <td contenteditable="true" class="editable text-center font-mono text-[9.5px]">${data.phone_parent || ''}</td>
                    <td class="no-print text-center border-0">
                        <button onclick="removeRow(this)" class="text-red-400 hover:text-red-700 font-bold px-1" title="លុប">✕</button>
                    </td>
                </tr>
            `;
        }

        function renderTable() {
            const tbody = document.getElementById('student-rows');
            const savedData = localStorage.getItem(`attendance_${currentYear}_${currentMonth}`);
            
            if (savedData) {
                const parsed = JSON.parse(savedData);
                document.getElementById('class_name').innerText = parsed.header.class_name || '';
                document.getElementById('building_name').innerText = parsed.header.building_name || '';
                document.getElementById('room_name').innerText = parsed.header.room_name || '';
                document.getElementById('teacher_name').innerText = parsed.header.teacher_name || '';
                document.getElementById('teacher_sex').innerText = parsed.header.teacher_sex || '';
                document.getElementById('doc_date').innerText = parsed.header.doc_date || '';
                document.getElementById('doc_time').innerText = parsed.header.doc_time || '';
                document.getElementById('phone_number').innerText = parsed.header.phone_number || '';
                
                tbody.innerHTML = '';
                parsed.students.forEach((s, idx) => {
                    tbody.innerHTML += createRowHTML(idx + 1, s);
                });
            } else {
                tbody.innerHTML = '';
                for (let i = 1; i <= 15; i++) {
                    tbody.innerHTML += createRowHTML(i);
                }
            }
        }

        function addNewRow() {
            const tbody = document.getElementById('student-rows');
            const nextIdx = tbody.children.length + 1;
            const temp = document.createElement('tbody');
            temp.innerHTML = createRowHTML(nextIdx);
            tbody.appendChild(temp.firstElementChild);
            saveData(false);
        }

        function removeRow(btn) {
            btn.closest('tr').remove();
            document.querySelectorAll('#student-rows tr').forEach((r, idx) => {
                r.children[0].innerText = idx + 1;
            });
            saveData(false);
        }

        function saveData(showAlert = false) {
            const header = {
                class_name: document.getElementById('class_name').innerText.trim(),
                building_name: document.getElementById('building_name').innerText.trim(),
                room_name: document.getElementById('room_name').innerText.trim(),
                teacher_name: document.getElementById('teacher_name').innerText.trim(),
                teacher_sex: document.getElementById('teacher_sex').innerText.trim(),
                doc_date: document.getElementById('doc_date').innerText.trim(),
                doc_time: document.getElementById('doc_time').innerText.trim(),
                phone_number: document.getElementById('phone_number').innerText.trim()
            };
            const students = [];
            document.querySelectorAll('#student-rows tr').forEach(r => {
                const days = [];
                for (let i = 3; i < 3 + daysInMonth; i++) {
                    days.push(r.children[i].innerText.trim());
                }
                students.push({
                    name: r.children[1].innerText.trim(),
                    sex: r.children[2].innerText.trim(),
                    days: days,
                    phone_student: r.children[3 + daysInMonth].innerText.trim(),
                    phone_parent: r.children[4 + daysInMonth].innerText.trim()
                });
            });

            localStorage.setItem(`attendance_${currentYear}_${currentMonth}`, JSON.stringify({ header, students }));
            if (showAlert) alert("✅ បានរក្សាទុកទិន្នន័យខែ " + khmerMonths[currentMonth] + " ដោយជោគជ័យ!");
        }

        // ការ Export ជារូបភាពធានាថាទិន្នន័យស្អាត មិនជាន់បន្ទាត់
        async function exportAsImage() {
            saveData(false);
            const btn = document.getElementById('btn-export-img');
            const originalText = btn.innerText;
            btn.innerText = "⏳ កំពុង Save...";
            btn.disabled = true;

            await document.fonts.ready;

            const captureArea = document.getElementById('capture-area');

            html2canvas(captureArea, {
                scale: 3, // Ultra-HD 300 DPI
                useCORS: true,
                allowTaint: true,
                backgroundColor: "#ffffff",
                logging: false,
                onclone: function(clonedDoc) {
                    const clonedCaptureArea = clonedDoc.getElementById('capture-area');
                    clonedCaptureArea.style.boxShadow = 'none';
                    clonedCaptureArea.style.margin = '0';

                    const clonedTable = clonedDoc.getElementById('main-table');
                    const originalTable = document.getElementById('main-table');
                    if (clonedTable && originalTable) {
                        clonedTable.style.width = originalTable.offsetWidth + 'px';
                        clonedTable.style.tableLayout = 'fixed';
                        clonedTable.style.border = '1.5px solid black';
                    }

                    // កម្ពស់ក្រឡា 34px
                    clonedDoc.querySelectorAll('.attendance-table tbody tr').forEach(tr => {
                        tr.style.height = '34px';
                    });

                    // ឈ្មោះសិស្ស៖ Siemreap, 16px, មិនដិត, ចំកណ្តាលក្រឡា
                    clonedDoc.querySelectorAll('.student-name-cell').forEach(cell => {
                        cell.style.fontFamily = "'Siemreap', sans-serif";
                        cell.style.fontSize = '16px';
                        cell.style.fontWeight = 'normal';
                        cell.style.lineHeight = 'normal';
                        cell.style.height = '34px';
                        cell.style.textAlign = 'center';
                        cell.style.verticalAlign = 'middle';
                        cell.style.padding = '2px 4px';
                        cell.style.borderBottom = '1px solid black';
                    });

                    // ព័ត៌មានគ្រូ & ប្រចាំខែ៖ ពណ៌ខ្មៅសុទ្ធ និងឃ្លាតពីបន្ទាត់ មិនជាន់ជើងអក្សរ
                    clonedDoc.querySelectorAll('.teacher-info-custom').forEach(el => {
                        el.style.fontFamily = "'Siemreap', sans-serif";
                        el.style.fontSize = '16px';
                        el.style.color = '#000000';
                    });

                    clonedDoc.querySelectorAll('.field-teacher-line').forEach(el => {
                        el.style.paddingBottom = '5px';
                        el.style.lineHeight = '1.2';
                        el.style.borderBottom = '1px dotted #000000';
                    });

                    const clonedMonth = clonedDoc.getElementById('khmer_month_label');
                    if (clonedMonth) {
                        clonedMonth.style.paddingBottom = '5px';
                        clonedMonth.style.lineHeight = '1.2';
                        clonedMonth.style.borderBottom = '1px dotted #000000';
                    }

                    clonedDoc.querySelectorAll('.day-cell').forEach(cell => {
                        cell.style.height = '34px';
                        cell.style.lineHeight = 'normal';
                        cell.style.verticalAlign = 'middle';
                        cell.style.textAlign = 'center';
                        cell.style.fontFamily = 'Arial, sans-serif';
                        cell.style.borderBottom = '1px solid black';
                    });
                }
            }).then(async canvas => {
                const fileName = `បញ្ជីវត្តមានសិស្ស_${khmerMonths[currentMonth]}_${currentYear}.png`;
                const imgDataUrl = canvas.toDataURL('image/png', 1.0);

                const isMobile = /Android|iPhone|iPad|iPod/i.test(navigator.userAgent);

                if (isMobile && navigator.canShare) {
                    canvas.toBlob(async (blob) => {
                        const file = new File([blob], fileName, { type: 'image/png' });
                        if (navigator.canShare({ files: [file] })) {
                            try {
                                await navigator.share({
                                    files: [file],
                                    title: 'បញ្ជីវត្តមានសិស្ស',
                                    text: fileName
                                });
                                return;
                            } catch (err) {}
                        }
                        showMobileModal(imgDataUrl, fileName);
                    }, 'image/png', 1.0);
                } else if (isMobile) {
                    showMobileModal(imgDataUrl, fileName);
                } else {
                    const link = document.createElement('a');
                    link.download = fileName;
                    link.href = imgDataUrl;
                    link.click();
                }
            }).catch(err => {
                alert("Error: " + err);
            }).finally(() => {
                btn.innerText = originalText;
                btn.disabled = false;
            });
        }

        function showMobileModal(imgSrc, fileName) {
            const modal = document.getElementById('mobile-save-modal');
            const preview = document.getElementById('mobile-preview-img');
            const downloadBtn = document.getElementById('mobile-download-link');
            
            preview.src = imgSrc;
            downloadBtn.href = imgSrc;
            downloadBtn.download = fileName;
            
            modal.style.display = 'flex';
        }

        function closeMobileModal() {
            document.getElementById('mobile-save-modal').style.display = 'none';
        }

        function resetData() {
            if (confirm("តើអ្នកចង់សម្អាតទិន្នន័យក្នុងខែនេះឡើងវិញមែនទេ?")) {
                localStorage.removeItem(`attendance_${currentYear}_${currentMonth}`);
                renderTable();
            }
        }

        window.onload = function () {
            loadSavedLogo();
            initYearOptions();
            changeCalendar();
            document.body.addEventListener('input', () => saveData(false));
        };
    </script>
</body>
</html>
"""

@app.route('/')
def index():
    return render_template_string(HTML_CODE)

if __name__ == '__main__':
    print("=" * 65)
    print("🚀 កំពុងដំណើរការប្រព័ន្ធគ្រប់គ្រងវត្តមានសិស្ស...")
    print("👉 សូមបើក Browser ចូលទៅកាន់: http://127.0.0.1:5000")
    print("=" * 65)
    app.run(debug=True, port=5000)