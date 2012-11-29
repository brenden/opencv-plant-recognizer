# Scripts for image matching
DESCRIBE = ../describeLeaves.py
MATCH = ../matchLeaves.py
GRADE = ../gradeMatch.py

# Intermediate result locations
PROBE_DATASET = datasets/flavia-mini-probes
GALLERY_DATASET = datasets/flavia-mini
PROBE_DESCRIPTORS = descriptors/flavia-mini-probes
GALLERY_DESCRIPTORS = descriptors/flavia-mini
MATCHES = matches.p
METRICS = metrics.p

# Dummy target files are used to control makefile flow
all: t-gis-dataset t-flavia-dataset t-gis-descriptors t-flavia-descriptors t-matches t-metrics
	
t-gis-dataset: 
	@echo "TODO"
	touch t-gis-dataset

t-flavia-dataset:
	@echo "TODO"
	touch t-flavia-dataset

t-gis-descriptors: t-gis-dataset
	mkdir -p $(PROBE_DESCRIPTORS)
	$(DESCRIBE) $(PROBE_DATASET) $(PROBE_DESCRIPTORS)
	touch t-gis-descriptors

t-flavia-descriptors: t-flavia-dataset	
	mkdir -p $(GALLERY_DESCRIPTORS)
	$(DESCRIBE) $(GALLERY_DATASET) $(GALLERY_DESCRIPTORS)
	touch t-flavia-descriptors

t-matches: t-flavia-descriptors t-gis-descriptors
	$(MATCH) $(GALLERY_DESCRIPTORS) $(PROBE_DESCRIPTORS) > $(MATCHES)
	touch t-matches

t-metrics: t-matches 
	$(GRADE) $(MATCHES) datasets/flavia/index.csv > $(METRICS)
	touch t-metrics

clean: 
	rm -f t-gis-dataset t-flavia-dataset t-gis-descriptors t-flavia-descriptors t-matches t-metrics
	rm -f $(MATCHES) $(METRICS)
	rm -rf $(PROBE_DESCRIPTORS) $(GALLERY_DESCRIPTORS)
