package com.example.quran

import android.content.Context
import android.graphics.BitmapFactory
import android.view.LayoutInflater
import android.view.View
import android.view.ViewGroup
import android.widget.ImageView
import androidx.recyclerview.widget.RecyclerView
import java.io.InputStream
import kotlin.math.ceil

class QuranPagerAdapter(
    private val context: Context,
    private val pages: List<String>,
    private val isLandscape: Boolean,
    private val onPageTapped: () -> Unit // Added tap listener
) : RecyclerView.Adapter<QuranPagerAdapter.PageViewHolder>() {

    class PageViewHolder(view: View) : RecyclerView.ViewHolder(view) {
        val rightImageView: ImageView = view.findViewById(R.id.rightPageImage)
        val leftImageView: ImageView = view.findViewById(R.id.leftPageImage)
    }

    override fun onCreateViewHolder(parent: ViewGroup, viewType: Int): PageViewHolder {
        val view = LayoutInflater.from(context).inflate(R.layout.item_page, parent, false)
        return PageViewHolder(view)
    }

    override fun onBindViewHolder(holder: PageViewHolder, position: Int) {
        holder.rightImageView.setImageDrawable(null)
        holder.leftImageView.setImageDrawable(null)

        // Make the whole page clickable to trigger the UI toggle
        holder.itemView.setOnClickListener {
            onPageTapped()
        }

        if (!isLandscape) {
            holder.leftImageView.visibility = View.GONE
            holder.rightImageView.visibility = View.VISIBLE
            holder.rightImageView.scaleType = ImageView.ScaleType.FIT_CENTER

            try {
                val stream: InputStream = context.assets.open("quran_pages/${pages[position]}")
                holder.rightImageView.setImageBitmap(BitmapFactory.decodeStream(stream))
            } catch (e: Exception) { e.printStackTrace() }

        } else {
            if (position == 0) {
                holder.leftImageView.visibility = View.GONE
                holder.rightImageView.visibility = View.VISIBLE
                holder.rightImageView.scaleType = ImageView.ScaleType.FIT_CENTER

                if (pages.isNotEmpty()) {
                    try {
                        val stream: InputStream = context.assets.open("quran_pages/${pages[0]}")
                        holder.rightImageView.setImageBitmap(BitmapFactory.decodeStream(stream))
                    } catch (e: Exception) { e.printStackTrace() }
                }
            } else {
                holder.leftImageView.visibility = View.VISIBLE
                holder.rightImageView.visibility = View.VISIBLE
                holder.rightImageView.scaleType = ImageView.ScaleType.FIT_START
                holder.leftImageView.scaleType = ImageView.ScaleType.FIT_END

                val rightIndex = (position * 2) - 1
                val leftIndex = position * 2

                if (rightIndex < pages.size) {
                    try {
                        val stream: InputStream = context.assets.open("quran_pages/${pages[rightIndex]}")
                        holder.rightImageView.setImageBitmap(BitmapFactory.decodeStream(stream))
                    } catch (e: Exception) { e.printStackTrace() }
                } else {
                    holder.rightImageView.visibility = View.INVISIBLE
                }

                if (leftIndex < pages.size) {
                    try {
                        val stream: InputStream = context.assets.open("quran_pages/${pages[leftIndex]}")
                        holder.leftImageView.setImageBitmap(BitmapFactory.decodeStream(stream))
                    } catch (e: Exception) { e.printStackTrace() }
                } else {
                    holder.leftImageView.visibility = View.INVISIBLE
                }
            }
        }
    }

    override fun getItemCount(): Int {
        if (pages.isEmpty()) return 0
        return if (isLandscape) {
            1 + ceil((pages.size - 1) / 2.0).toInt()
        } else {
            pages.size
        }
    }
}