---
title: {{ .Title | jsonify }}
date: {{ .Date.Format "2006-01-02" }}
description: {{ .Description | jsonify }}
---
{{ .RawContent }}
