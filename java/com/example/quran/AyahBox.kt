package com.example.quran

// This represents a single highlight box for an Ayah
data class AyahBox(
    val x: Int,
    val y: Int,
    val w: Int,
    val h: Int,
    val id: String
)