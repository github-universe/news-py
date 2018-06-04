CREATE TABLE `news_news` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `title` varchar(255) NOT NULL,
  `content` varchar(4000) NOT NULL,
  `created` datetime(6) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

CREATE TABLE `news_keyword` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `keyword` varchar(255) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

CREATE TABLE `news_newskeyword` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `keyword_id` int(11) NOT NULL,
  `news_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `news_newskeyword_keyword_id_00903b4f_fk_news_keyword_id` (`keyword_id`),
  KEY `news_newskeyword_news_id_e0ef167f_fk_news_news_id` (`news_id`),
  CONSTRAINT `news_newskeyword_keyword_id_00903b4f_fk_news_keyword_id` FOREIGN KEY (`keyword_id`) REFERENCES `news_keyword` (`id`),
  CONSTRAINT `news_newskeyword_news_id_e0ef167f_fk_news_news_id` FOREIGN KEY (`news_id`) REFERENCES `news_news` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

CREATE TABLE `news_newspatent` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `patent_id` varchar(255) NOT NULL,
  `news_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `news_newspatent_news_id_0caea342_fk_news_news_id` (`news_id`),
  CONSTRAINT `news_newspatent_news_id_0caea342_fk_news_news_id` FOREIGN KEY (`news_id`) REFERENCES `news_news` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=272 DEFAULT CHARSET=utf8;