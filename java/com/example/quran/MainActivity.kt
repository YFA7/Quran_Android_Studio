package com.example.quran

import android.app.Dialog
import android.content.Context
import android.content.res.Configuration
import android.os.Build
import android.os.Bundle
import android.view.View
import android.view.WindowManager
import android.widget.ArrayAdapter
import android.widget.ImageView
import android.widget.LinearLayout
import android.widget.ListView
import android.widget.SeekBar
import android.widget.TextView
import androidx.appcompat.app.AppCompatActivity
import androidx.cardview.widget.CardView
import androidx.core.view.WindowCompat
import androidx.core.view.WindowInsetsCompat
import androidx.core.view.WindowInsetsControllerCompat
import androidx.viewpager2.widget.ViewPager2
import kotlin.math.ceil

class MainActivity : AppCompatActivity() {

    // حروف الفهرس والخاتمة
    private val abjadLetters = listOf("أ", "ب", "ج", "د", "هـ", "و", "ز", "ح", "ط", "ى", "ك", "ل")

    // هيكل بيانات السورة
    private data class SurahInfo(val number: Int, val name: String, val startPage: Int)

    // قائمة الـ 114 سورة
    private val surahsList = listOf(
        SurahInfo(1, "الفاتحة", 1), SurahInfo(2, "البقرة", 2), SurahInfo(3, "آل عمران", 50),
        SurahInfo(4, "النساء", 77), SurahInfo(5, "المائدة", 106), SurahInfo(6, "الأنعام", 128),
        SurahInfo(7, "الأعراف", 151), SurahInfo(8, "الأنفال", 177), SurahInfo(9, "التوبة", 187),
        SurahInfo(10, "يونس", 208), SurahInfo(11, "هود", 221), SurahInfo(12, "يوسف", 235),
        SurahInfo(13, "الرعد", 249), SurahInfo(14, "إبراهيم", 255), SurahInfo(15, "الحجر", 262),
        SurahInfo(16, "النحل", 267), SurahInfo(17, "الإسراء", 282), SurahInfo(18, "الكهف", 293),
        SurahInfo(19, "مريم", 305), SurahInfo(20, "طه", 312), SurahInfo(21, "الأنبياء", 322),
        SurahInfo(22, "الحج", 332), SurahInfo(23, "المؤمنون", 342), SurahInfo(24, "النور", 350),
        SurahInfo(25, "الفرقان", 359), SurahInfo(26, "الشعراء", 367), SurahInfo(27, "النمل", 377),
        SurahInfo(28, "القصص", 385), SurahInfo(29, "العنكبوت", 396), SurahInfo(30, "الروم", 404),
        SurahInfo(31, "لقمان", 411), SurahInfo(32, "السجدة", 415), SurahInfo(33, "الأحزاب", 418),
        SurahInfo(34, "سبأ", 428), SurahInfo(35, "فاطر", 434), SurahInfo(36, "يس", 440),
        SurahInfo(37, "الصافات", 446), SurahInfo(38, "ص", 453), SurahInfo(39, "الزمر", 458),
        SurahInfo(40, "غافر", 467), SurahInfo(41, "فصلت", 477), SurahInfo(42, "الشورى", 483),
        SurahInfo(43, "الزخرف", 489), SurahInfo(44, "الدخان", 496), SurahInfo(45, "الجاثية", 499),
        SurahInfo(46, "الأحقاف", 502), SurahInfo(47, "محمد", 507), SurahInfo(48, "الفتح", 511),
        SurahInfo(49, "الحجرات", 515), SurahInfo(50, "ق", 518), SurahInfo(51, "الذاريات", 520),
        SurahInfo(52, "الطور", 523), SurahInfo(53, "النجم", 526), SurahInfo(54, "القمر", 528),
        SurahInfo(55, "الرحمن", 531), SurahInfo(56, "الواقعة", 534), SurahInfo(57, "الحديد", 537),
        SurahInfo(58, "المجادلة", 542), SurahInfo(59, "الحشر", 545), SurahInfo(60, "الممتحنة", 549),
        SurahInfo(61, "الصف", 551), SurahInfo(62, "الجمعة", 553), SurahInfo(63, "المنافقون", 554),
        SurahInfo(64, "التغابن", 556), SurahInfo(65, "الطلاق", 558), SurahInfo(66, "التحريم", 560),
        SurahInfo(67, "الملك", 562), SurahInfo(68, "القلم", 564), SurahInfo(69, "الحاقة", 566),
        SurahInfo(70, "المعارج", 568), SurahInfo(71, "نوح", 570), SurahInfo(72, "الجن", 572),
        SurahInfo(73, "المزمل", 574), SurahInfo(74, "المدثر", 575), SurahInfo(75, "القيامة", 577),
        SurahInfo(76, "الإنسان", 578), SurahInfo(77, "المرسلات", 580), SurahInfo(78, "النبأ", 582),
        SurahInfo(79, "النازعات", 583), SurahInfo(80, "عبس", 585), SurahInfo(81, "التكوير", 586),
        SurahInfo(82, "الانفطار", 587), SurahInfo(83, "المطففين", 587), SurahInfo(84, "الانشقاق", 589),
        SurahInfo(85, "البروج", 590), SurahInfo(86, "الطارق", 591), SurahInfo(87, "الأعلى", 591),
        SurahInfo(88, "الغاشية", 592), SurahInfo(89, "الفجر", 593), SurahInfo(90, "البلد", 594),
        SurahInfo(91, "الشمس", 595), SurahInfo(92, "الليل", 595), SurahInfo(93, "الضحى", 596),
        SurahInfo(94, "الشرح", 596), SurahInfo(95, "التين", 597), SurahInfo(96, "العلق", 597),
        SurahInfo(97, "القدر", 598), SurahInfo(98, "البينة", 598), SurahInfo(99, "الزلزلة", 599),
        SurahInfo(100, "العاديات", 599), SurahInfo(101, "القارعة", 600), SurahInfo(102, "التكاثر", 600),
        SurahInfo(103, "العصر", 601), SurahInfo(104, "الهمزة", 601), SurahInfo(105, "الفيل", 601),
        SurahInfo(106, "قريش", 602), SurahInfo(107, "الماعون", 602), SurahInfo(108, "الكوثر", 602),
        SurahInfo(109, "الكافرون", 603), SurahInfo(110, "النصر", 603), SurahInfo(111, "المسد", 603),
        SurahInfo(112, "الإخلاص", 604), SurahInfo(113, "الفلق", 604), SurahInfo(114, "الناس", 604)
    )

    // متغيرات التحكم
    private var isUiVisible = true
    private var lastVisitedPosition = -1

    // عناصر الواجهة
    private lateinit var viewPager: ViewPager2
    private lateinit var bottomUiContainer: CardView
    private lateinit var topUiContainer: CardView
    private lateinit var dragPopupLayout: LinearLayout
    private lateinit var popupSurahText: TextView
    private lateinit var popupPageText: TextView

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)

        // إعدادات الشاشة الكاملة
        WindowCompat.setDecorFitsSystemWindows(window, false)
        window.addFlags(WindowManager.LayoutParams.FLAG_KEEP_SCREEN_ON)

        if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.P) {
            window.attributes.layoutInDisplayCutoutMode = WindowManager.LayoutParams.LAYOUT_IN_DISPLAY_CUTOUT_MODE_SHORT_EDGES
        }
        window.statusBarColor = android.graphics.Color.TRANSPARENT
        window.navigationBarColor = android.graphics.Color.TRANSPARENT

        setContentView(R.layout.activity_main)

        // ربط العناصر
        viewPager = findViewById(R.id.viewPager)
        bottomUiContainer = findViewById(R.id.bottomUiContainer)
        topUiContainer = findViewById(R.id.topUiContainer)
        dragPopupLayout = findViewById(R.id.dragPopupLayout)
        popupSurahText = findViewById(R.id.popupSurahText)
        popupPageText = findViewById(R.id.popupPageText)

        val pageSeekBar: SeekBar = findViewById(R.id.pageSeekBar)
        val btnReturn: ImageView = findViewById(R.id.btnReturn)
        val btnIndex: ImageView = findViewById(R.id.btnIndex)

        viewPager.isSaveEnabled = false

        // قراءة مجلد الصور
        val pagesList = mutableListOf<String>()
        try {
            val files = assets.list("quran_pages")
            if (files != null) {
                val filteredFiles = files.filter { it.startsWith("A_") || it.startsWith("B_") || it.startsWith("C_") }.sorted()
                pagesList.addAll(filteredFiles)
            }
        } catch (e: Exception) { e.printStackTrace() }

        // التحقق من اتجاه الشاشة
        val isLandscape = resources.configuration.orientation == Configuration.ORIENTATION_LANDSCAPE

        // إعداد ViewPager
        val adapter = QuranPagerAdapter(this, pagesList, isLandscape) {
            toggleSystemUI()
        }
        viewPager.adapter = adapter

        // حساب عدد الصفحات للمقدمة والمصحف
        val introCount = pagesList.count { it.startsWith("A_") }
        val quranPageCount = pagesList.count { it.startsWith("B_") }
        val firstQuranSpreadPosition = (introCount + 1) / 2

        // استعادة آخر صفحة
        val sharedPrefs = getSharedPreferences("QuranAppPrefs", Context.MODE_PRIVATE)
        val savedAbsolutePage = sharedPrefs.getInt("LAST_SAVED_ABSOLUTE_PAGE", -1)
        if (savedAbsolutePage != -1) {
            val targetPosition = if (isLandscape) (savedAbsolutePage + 1) / 2 else savedAbsolutePage
            if (targetPosition < adapter.itemCount) {
                viewPager.post { viewPager.setCurrentItem(targetPosition, false) }
            }
        }

        bottomUiContainer.post { toggleSystemUI() }

        // زر العودة
        btnReturn.setOnClickListener {
            if (lastVisitedPosition != -1) {
                val currentPos = viewPager.currentItem
                viewPager.setCurrentItem(lastVisitedPosition, false)
                lastVisitedPosition = currentPos
            }
        }

        // زر الفهرس
        btnIndex.setOnClickListener {
            showIndexDialog(introCount, isLandscape)
        }

        // منطق التمرير والحفظ حسب الوضع
        if (isLandscape) {
            // إعداد التمرير الأفقي
            val quranSpreads = ceil(quranPageCount / 2.0).toInt()
            pageSeekBar.max = if (quranSpreads > 0) quranSpreads - 1 else 0

            viewPager.registerOnPageChangeCallback(object : ViewPager2.OnPageChangeCallback() {
                override fun onPageSelected(position: Int) {
                    val rightIndex = if (position == 0) 0 else (position * 2) - 1
                    sharedPrefs.edit().putInt("LAST_SAVED_ABSOLUTE_PAGE", rightIndex).apply()
                    val currentSpread = position - firstQuranSpreadPosition
                    pageSeekBar.progress = currentSpread.coerceIn(0, pageSeekBar.max)
                }
            })

            pageSeekBar.setOnSeekBarChangeListener(object : SeekBar.OnSeekBarChangeListener {
                override fun onProgressChanged(seekBar: SeekBar?, progress: Int, fromUser: Boolean) {
                    if (fromUser) {
                        val targetSpread = progress + firstQuranSpreadPosition
                        viewPager.setCurrentItem(targetSpread, false)
                        updatePopupContent(targetSpread, introCount, quranPageCount, pagesList, true)
                    }
                }
                override fun onStartTrackingTouch(seekBar: SeekBar?) {
                    lastVisitedPosition = viewPager.currentItem
                    dragPopupLayout.visibility = View.VISIBLE
                    val progress = seekBar?.progress ?: 0
                    updatePopupContent(progress + firstQuranSpreadPosition, introCount, quranPageCount, pagesList, true)
                }
                override fun onStopTrackingTouch(seekBar: SeekBar?) { dragPopupLayout.visibility = View.GONE }
            })

        } else {
            // إعداد التمرير العمودي
            pageSeekBar.max = if (quranPageCount > 0) quranPageCount - 1 else 0

            viewPager.registerOnPageChangeCallback(object : ViewPager2.OnPageChangeCallback() {
                override fun onPageSelected(position: Int) {
                    sharedPrefs.edit().putInt("LAST_SAVED_ABSOLUTE_PAGE", position).apply()
                    val currentQuranPage = position - introCount
                    pageSeekBar.progress = currentQuranPage.coerceIn(0, pageSeekBar.max)
                }
            })

            pageSeekBar.setOnSeekBarChangeListener(object : SeekBar.OnSeekBarChangeListener {
                override fun onProgressChanged(seekBar: SeekBar?, progress: Int, fromUser: Boolean) {
                    if (fromUser) {
                        val targetPage = progress + introCount
                        viewPager.setCurrentItem(targetPage, false)
                        updatePopupContent(targetPage, introCount, quranPageCount, pagesList, false)
                    }
                }
                override fun onStartTrackingTouch(seekBar: SeekBar?) {
                    lastVisitedPosition = viewPager.currentItem
                    dragPopupLayout.visibility = View.VISIBLE
                    val progress = seekBar?.progress ?: 0
                    updatePopupContent(progress + introCount, introCount, quranPageCount, pagesList, false)
                }
                override fun onStopTrackingTouch(seekBar: SeekBar?) { dragPopupLayout.visibility = View.GONE }
            })
        }
    }

    // دالة نافذة الفهرس
    private fun showIndexDialog(introCount: Int, isLandscape: Boolean) {
        val dialog = Dialog(this)
        dialog.setContentView(R.layout.dialog_index)

        dialog.window?.setBackgroundDrawableResource(android.R.color.transparent)
        dialog.window?.setLayout(
            (resources.displayMetrics.widthPixels * 0.6).toInt(),
            (resources.displayMetrics.heightPixels * 0.8).toInt()
        )

        val listView: ListView = dialog.findViewById(R.id.surahListView)

        // إعداد نصوص القائمة
        val displayList = surahsList.mapIndexed { index, surah ->
            val start = surah.startPage
            val end = if (index < surahsList.size - 1) {
                val nextStart = surahsList[index + 1].startPage
                if (nextStart > start) nextStart - 1 else start
            } else {
                604
            }

            val num = toArabicNumerals(surah.number)
            val sPage = toArabicNumerals(start)
            val ePage = toArabicNumerals(end)

            if (start == end) "$num.  ${surah.name} [$sPage]"
            else "$num.  ${surah.name} [$sPage-$ePage]"
        }

        val adapter = ArrayAdapter(this, R.layout.item_surah, R.id.surahNameText, displayList)
        listView.adapter = adapter

        // حساب السورة الحالية لفتح القائمة عليها
        val currentPos = viewPager.currentItem
        var currentQuranPage = 0

        if (isLandscape) {
            val firstQuranSpreadPosition = (introCount + 1) / 2
            val currentSpread = currentPos - firstQuranSpreadPosition
            if (currentSpread >= 0) currentQuranPage = (currentSpread * 2) + 1
        } else {
            currentQuranPage = currentPos - introCount + 1
        }

        var currentSurahIndex = 0
        for (i in surahsList.indices) {
            if (currentQuranPage >= surahsList[i].startPage) currentSurahIndex = i
            else break
        }

        // تمرير القائمة تلقائياً للسورة الحالية
        listView.setSelection(currentSurahIndex)

        // الانتقال عند النقر على سورة
        listView.setOnItemClickListener { _, _, position, _ ->
            val targetPage = surahsList[position].startPage
            val absoluteListIndex = introCount + targetPage - 1
            lastVisitedPosition = viewPager.currentItem

            val targetViewPagerPosition = if (isLandscape) (absoluteListIndex + 1) / 2 else absoluteListIndex

            viewPager.setCurrentItem(targetViewPagerPosition, false)
            dialog.dismiss()
        }

        dialog.show()
    }

    // إظهار وإخفاء القوائم والشريط العلوي
    private fun toggleSystemUI() {
        val windowInsetsController = WindowInsetsControllerCompat(window, window.decorView)
        isUiVisible = !isUiVisible

        if (isUiVisible) {
            windowInsetsController.show(WindowInsetsCompat.Type.systemBars())
            bottomUiContainer.animate().translationY(0f).setDuration(250).start()
            topUiContainer.animate().translationY(0f).setDuration(250).start()
        } else {
            windowInsetsController.hide(WindowInsetsCompat.Type.systemBars())
            bottomUiContainer.animate().translationY(bottomUiContainer.height.toFloat() + 150f).setDuration(250).start()
            topUiContainer.animate().translationY(-(topUiContainer.height.toFloat() + 150f)).setDuration(250).start()
        }
    }

    // تحديث النافذة المنبثقة عند السحب
    private fun updatePopupContent(position: Int, introCount: Int, quranPageCount: Int, pagesList: List<String>, isLandscape: Boolean) {
        if (isLandscape) {
            if (position == 0) {
                popupSurahText.text = "المقدمة"
                popupPageText.text = ""
                return
            }

            val rightIndex = (position * 2) - 1
            val leftIndex = position * 2
            val rightFileName = pagesList.getOrNull(rightIndex) ?: ""
            val leftFileName = pagesList.getOrNull(leftIndex) ?: ""

            when {
                rightFileName.startsWith("B_") || leftFileName.startsWith("B_") -> {
                    val rPage = if (rightFileName.startsWith("B_")) (rightIndex - introCount + 1) else 0
                    val lPage = if (leftFileName.startsWith("B_")) (leftIndex - introCount + 1) else 0

                    popupSurahText.text = getSurahName(if (rPage > 0) rPage else lPage)

                    if (rPage > 0 && lPage > 0) popupPageText.text = "${toArabicNumerals(rPage)} - ${toArabicNumerals(lPage)}"
                    else if (rPage > 0) popupPageText.text = toArabicNumerals(rPage)
                    else if (lPage > 0) popupPageText.text = toArabicNumerals(lPage)
                }
                rightFileName.startsWith("C_") || leftFileName.startsWith("C_") -> {
                    popupSurahText.text = "الخاتمة / الفهرس"
                    val rIndex = if (rightFileName.startsWith("C_")) rightIndex - introCount - quranPageCount else -1
                    val lIndex = if (leftFileName.startsWith("C_")) leftIndex - introCount - quranPageCount else -1
                    val rText = if (rIndex in abjadLetters.indices) abjadLetters[rIndex] else ""
                    val lText = if (lIndex in abjadLetters.indices) abjadLetters[lIndex] else ""
                    popupPageText.text = "$rText - $lText"
                }
                else -> {
                    popupSurahText.text = "المقدمة"
                    popupPageText.text = ""
                }
            }
        } else {
            val fileName = pagesList.getOrNull(position) ?: ""
            when {
                fileName.startsWith("A_") -> {
                    popupSurahText.text = "المقدمة"
                    popupPageText.text = ""
                }
                fileName.startsWith("B_") -> {
                    val actualPageNum = position - introCount + 1
                    popupSurahText.text = getSurahName(actualPageNum)
                    popupPageText.text = toArabicNumerals(actualPageNum)
                }
                fileName.startsWith("C_") -> {
                    popupSurahText.text = "الخاتمة / الفهرس"
                    val cIndex = position - introCount - quranPageCount
                    popupPageText.text = if (cIndex in abjadLetters.indices) abjadLetters[cIndex] else ""
                }
                else -> {
                    popupSurahText.text = ""
                    popupPageText.text = ""
                }
            }
        }
    }

    // جلب اسم السورة حسب رقم الصفحة
    private fun getSurahName(page: Int): String {
        var currentSurah = "الفاتحة"
        for (surah in surahsList) {
            if (page >= surah.startPage) currentSurah = surah.name
            else break
        }
        return currentSurah
    }

    // تحويل الأرقام الإنجليزية إلى عربية
    private fun toArabicNumerals(number: Int): String {
        val arabicChars = charArrayOf('٠', '١', '٢', '٣', '٤', '٥', '٦', '٧', '٨', '٩')
        val builder = StringBuilder()
        for (char in number.toString()) {
            if (char.isDigit()) builder.append(arabicChars[char - '0'])
            else builder.append(char)
        }
        return builder.toString()
    }
}