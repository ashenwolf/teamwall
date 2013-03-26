(ns teamwall.base)

(.ready (js/jQuery js/document)
	(fn []
		(.click (js/jQuery "a#logout-link")
			(fn []
				(do (.submit (aget (.-forms js/document) "logout-form"))
					false)))))
