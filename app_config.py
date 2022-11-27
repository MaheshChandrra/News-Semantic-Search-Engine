DATASET_DRIVE_LINK="https://drive.google.com/uc?id=1-yEN_RzagNAsB5tBNTuEwRIlZWtl4RzC&confirm=t&uuid=45bf30c4-bc5d-4485-aa37-6b1689ec5ea0&at=AHV7M3eLkHtHSyPzjOByoJbCY2qy:1669362146129"#"https://drive.google.com/uc?id=1-yEN_RzagNAsB5tBNTuEwRIlZWtl4RzC&confirm=t"
GDRIVE_DATASET_ID="1-yEN_RzagNAsB5tBNTuEwRIlZWtl4RzC"
DATSET_FILE_NAME="news_data_with_embeddings.pkl"
DATASET_PATH="datasets/"

BOOTSTRAP_CARD_TAG=tag="""
      <div class="preview-card">
        <div class="preview-card__wrp">
          <div class="preview-card__item swiper-slide">
            <div class="preview-card__img">
              <img src="https://s.wordpress.com/mshots/v1/{formatted_link}"alt="">
            </div>
            <div class="preview-card__content">
              <span class="preview-card__code">{date}</span>
              <p><strong>Closest match: {closest_match:.2f}%</strong></p>
              <div class="preview-card__title">{headline}</div>
              <div class="preview-card__text">{short_description}</div>
              <a href="{link}" class="preview-card__button">READ MORE</a>
            </div>
          </div>
          </div>
          </div>
"""