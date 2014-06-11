create table rssTables (
	feed_id  bigint not null auto_increment,
	author  text CHARACTER SET utf8,
	author_detail  text CHARACTER SET utf8,
	authors  text CHARACTER SET utf8,
	docs  text CHARACTER SET utf8,
	generator  text CHARACTER SET utf8,
	generator_detail  text CHARACTER SET utf8,
	language  text CHARACTER SET utf8,
	link  text CHARACTER SET utf8,
	links  text CHARACTER SET utf8,
	published  DATETIME,
	subtitle  text CHARACTER SET utf8,
	subtitle_detail  text CHARACTER SET utf8,
	title  text CHARACTER SET utf8,
	title_detail  text CHARACTER SET utf8,
	updated  DATETIME,
	primary key(feed_id)
);

create table rssArticlesDescription (
	articleDesc_id bigint not null auto_increment,
	feed_id  bigint not null,
	id text CHARACTER SET utf8,
	author text CHARACTER SET utf8,
	author_detail  text CHARACTER SET utf8,
	authors  text CHARACTER SET utf8,
	link  text CHARACTER SET utf8,
	links  text CHARACTER SET utf8,
	title  text CHARACTER SET utf8,
	title_detail  text CHARACTER SET utf8,
	summary  text CHARACTER SET utf8,
	published  DATETIME,
	guidislink bool,
	primary key(articleDesc_id)
);

create table rssArticles (
	article_id bigint not null auto_increment,
	articleDesc_id bigint not null,
	feed_id  bigint not null,
	link text CHARACTER SET utf8,
	parseDate DATETIME,
	rssTitle text CHARACTER SET utf8,
	parsedTitle text CHARACTER SET utf8,
	content  text CHARACTER SET utf8,
	primary key(article_id)
);

create table articlesAnaSum (
	articlesAnaSum_id bigint not null auto_increment,
	article_id bigint not null,
	POSTags text CHARACTER SET utf8,
	NERTagsEn text CHARACTER SET utf8,
	NERTagsGe text CHARACTER SET utf8,
	primary key(articlesAnaSum_id)
);

create table words (
	word_id bigint not null auto_increment,
	articlesAnaSum_id bigint not null,
	word text CHARACTER SET utf8,
	POSTag text CHARACTER SET utf8,
	NERTagEn text CHARACTER SET utf8,
	NERTagGe text CHARACTER SET utf8,
	primary key(word_id)
);

create table simpleAnaLocations (
	simpleAnaLocations_id bigint not null auto_increment,
	article_id bigint not null,
	locationText text CHARACTER SET utf8,
	locationJson text CHARACTER SET utf8,
	articleTitle text CHARACTER SET utf8,
	published DATETIME not null,
	lon real not null,
	lat real not null,
	primary key(simpleAnaLocations_id)
);
