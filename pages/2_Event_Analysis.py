# Main screen: event, analogues, outcomes, context, confidence and source.
import streamlit as st
from src.ui.copy import DISCLAIMER,EVIDENCE_MESSAGES
from src.ui.mock_data import SAMPLE_EVENT
st.title('Event Analysis')
# TODO: replace mock with read-only Supabase query; add event/horizon/benchmark controls.
# Add analogue distribution, TUPRS/XU100 chart, macro context, confidence and source.
event=SAMPLE_EVENT
st.subheader(event['title'])
st.write(EVIDENCE_MESSAGES[event['evidence_direction']])
c=st.columns(3)
c[0].metric('Similar Historical Events',event['analogue_count'])
c[1].metric('Median 3D Abnormal Return',f"{event['median_abnormal_return_3d']:.2%}")
c[2].metric('Positive Outcome Ratio',f"{event['positive_ratio_3d']:.1%}")
st.caption(DISCLAIMER)
