import { Swiper, SwiperSlide } from 'swiper/react'
import styles from '/styles/components/utils/PosterSlider.module.scss'
import Image from "next/image"
import Link from "next/link"


const PosterSlider = ({medias, title, type='movie', preload = false}) => {
    return (
        <div className={styles.slider_container}>
            {title && <p className={styles.slider_title}>{title}</p>}
            <Swiper spaceBetween={10} slidesPerView={'auto'} className={styles.slider_body}>
                {medias && medias.map((media, index) => (
                    <SwiperSlide className={styles.slider_card} key={index}>
                        <Link href={`/${type}/${media.tmdb_id}`}>
                            {media.poster_image && <Image priority={preload} layout="fill" src={media.poster_image} />}
                        </Link>
                    </SwiperSlide>
                ))}
            </Swiper>
        </div>
    )
}

export default PosterSlider